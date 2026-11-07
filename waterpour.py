
import streamlit as st
import datetime
import time

st.set_page_config(
    page_title="Cold Water Pouring",
    page_icon="💧",
    layout="centered"
)

# -----------------------------
# 세션 초기화
# -----------------------------

defaults = {
    "alarm_at": None,
    "alarm_mode": "기본 모드",
    "no_spray": False,
    "alarm_triggered": False,
    "spray_started": False,
    "alarm_active": False,
    "message": "",
    "running": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# -----------------------------
# 디자인
# -----------------------------

st.markdown("""
<style>
.stApp {
    background: #e8f7ff;
    color: #172d40;
}

.main .block-container {
    max-width: 750px;
    padding-top: 40px;
}

h1, h2, h3, p, label {
    color: #172d40 !important;
}

.header {
    text-align: center;
    font-size: 45px;
    font-weight: 900;
    color: #168bc4;
}

.subtitle {
    text-align: center;
    font-size: 17px;
    margin-bottom: 30px;
}

.panel {
    background: white;
    border: 2px solid #9bdafa;
    border-radius: 20px;
    padding: 23px;
    margin: 15px 0;
}

.warning {
    background: #fff2dc;
    border: 2px solid #efa93e;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    font-weight: bold;
}

.spray {
    font-size: 100px;
    text-align: center;
    animation: splash 0.7s infinite alternate;
}

@keyframes splash {
    from {
        transform: scale(0.7);
    }
    to {
        transform: scale(1.3);
    }
}

.stButton button {
    background: #168bc4;
    color: white;
    border-radius: 12px;
    border: none;
    height: 50px;
    font-weight: bold;
}

.stButton button:hover {
    background: #086c9f;
    color: white;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# 제목
# -----------------------------

st.markdown(
    '<div class="header">💧 COLD WATER POURING</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">늦잠과의 전쟁, 이제 끝내자!</div>',
    unsafe_allow_html=True
)


# -----------------------------
# 알람 설정 화면
# -----------------------------

if not st.session_state.running:

    st.markdown("## ⏰ 알람 설정")

    with st.form("alarm_form"):

        alarm_time = st.time_input(
            "기상 시간",
            value=datetime.time(7, 0)
        )

        mode = st.radio(
            "작동 모드 선택",
            ["기본 모드", "특수 모드"],
            captions=[
                "알람 후 15초 뒤 화면 효과 실행",
                "알람 시간에 즉시 화면 효과 실행"
            ]
        )

        no_spray = st.checkbox(
            "💧 물 분사 효과 사용 안 함",
            value=False
        )

        submitted = st.form_submit_button(
            "알람 설정하기",
            use_container_width=True
        )

    if submitted:

        now = datetime.datetime.now()

        alarm_datetime = datetime.datetime.combine(
            now.date(),
            alarm_time
        )

        if alarm_datetime <= now:
            alarm_datetime += datetime.timedelta(days=1)

        st.session_state.alarm_at = alarm_datetime
        st.session_state.alarm_mode = mode
        st.session_state.no_spray = no_spray

        st.session_state.alarm_triggered = False
        st.session_state.spray_started = False
        st.session_state.alarm_active = False
        st.session_state.message = ""
        st.session_state.running = True

        st.rerun()


# -----------------------------
# 알람 대기 및 실행 화면
# -----------------------------

if st.session_state.running:

    @st.fragment(run_every="1s")
    def alarm_screen():

        now = datetime.datetime.now()
        alarm_at = st.session_state.alarm_at

        # 알람 시간 도달
        if now >= alarm_at and not st.session_state.alarm_triggered:

            st.session_state.alarm_triggered = True
            st.session_state.alarm_active = True

            if st.session_state.alarm_mode == "특수 모드":
                if st.session_state.no_spray:
                    st.session_state.message = "알람이 울렸습니다! 분사 효과는 꺼져 있습니다."
                else:
                    st.session_state.spray_started = True
                    st.session_state.message = "특수 모드 실행!"

        # 기본 모드 15초 대기
        if (
            st.session_state.alarm_triggered
            and st.session_state.alarm_mode == "기본 모드"
            and not st.session_state.spray_started
            and not st.session_state.no_spray
        ):

            elapsed = (
                now - alarm_at
            ).total_seconds()

            if elapsed >= 15:
                st.session_state.spray_started = True
                st.session_state.message = "기본 모드 실행!"

        # 대기 화면
        if not st.session_state.alarm_triggered:

            remaining = max(
                0,
                int((alarm_at - now).total_seconds())
            )

            hours = remaining // 3600
            minutes = (remaining % 3600) // 60
            seconds = remaining % 60

            st.markdown("""
            <div class="panel">
                <h2 style="text-align:center">
                    ⏳ 알람 대기 중
                </h2>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(
                f"### ⏰ 설정 시간: {alarm_at.strftime('%H:%M')}"
            )

            st.markdown(
                f"<h1 style='text-align:center;font-size:50px'>"
                f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                f"</h1>",
                unsafe_allow_html=True
            )

            st.write(f"모드: **{st.session_state.alarm_mode}**")

            st.info("설정한 시간까지 기다리는 중입니다.")

        # 알람 실행
        else:

            st.markdown("## 🚨 WAKE UP!")

            st.error("알람 시간이 되었습니다!")

            if st.session_state.no_spray:

                st.markdown("""
                <div class="panel">
                    <h2 style="text-align:center">
                        🔔 알람 실행 완료
                    </h2>
                    <p style="text-align:center">
                        물 분사 효과가 비활성화되어 있습니다.
                    </p>
                </div>
                """, unsafe_allow_html=True)

            elif st.session_state.spray_started:

                st.markdown("""
                <div class="spray">💦💧🌊</div>
                <h2 style="text-align:center">
                    WAKE UP!!
                </h2>
                """, unsafe_allow_html=True)

                st.success("화면 분사 효과가 실행되었습니다!")

            else:

                st.markdown("""
                <div class="warning">
                    ⚠️ 15초 후 화면 분사 효과가 실행됩니다!
                </div>
                """, unsafe_allow_html=True)

                elapsed = (
                    now - alarm_at
                ).total_seconds()

                st.markdown(
                    f"### 남은 시간: {max(0, 15-int(elapsed))}초"
                )

        # 마무리 경고
        if st.session_state.alarm_triggered:

            st.divider()

            st.markdown("""
            <div class="warning">
                ⚠️ 작동 안내<br><br>
                화면에 분사 애니메이션이 표시됩니다.<br>
                실제 액체를 분사하는 기능은 없습니다.<br>
                뜨거운 액체나 화학물질은 절대 사용하지 않습니다.
            </div>
            """, unsafe_allow_html=True)

            if st.button(
                "알람 종료 및 처음으로",
                use_container_width=True
            ):

                st.session_state.running = False
                st.session_state.alarm_at = None
                st.session_state.alarm_triggered = False
                st.session_state.spray_started = False
                st.session_state.alarm_active = False

                st.rerun()

    alarm_screen()


# -----------------------------
# 하단 안내
# -----------------------------

st.divider()

st.caption(
    "COLD WATER POURING | Wake up on time!"
)

st.caption(
    "알람은 앱과 브라우저가 실행 중일 때 작동합니다."
)
