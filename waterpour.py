
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo
import time as time_module

st.set_page_config(
    page_title="Cold Water Pouring",
    page_icon="💦",
    layout="centered"
)

KST = ZoneInfo("Asia/Seoul")

st.markdown("""
<style>
.stApp {
    background-color: #b9e8ff;
    color: black;
}
h1, h2, h3, p, label {
    color: black !important;
}
.stButton button {
    background-color: white;
    color: black;
    border-radius: 12px;
    border: 2px solid #333;
    font-weight: bold;
}
.splash {
    font-size: 75px;
    text-align: center;
    animation: splash 0.7s infinite alternate;
}
@keyframes splash {
    from {transform: scale(0.8);}
    to {transform: scale(1.2);}
}
</style>
""", unsafe_allow_html=True)

st.title("💦 Cold Water Pouring")
st.caption("늦잠 방지 프로젝트")

now = datetime.now(KST)
st.subheader("현재 한국 시간")
st.markdown(f"### 🕒 {now.strftime('%Y년 %m월 %d일 %H:%M:%S')}")

# 세션 상태 초기화
if "running" not in st.session_state:
    st.session_state.running = False

if "alarm_datetime" not in st.session_state:
    st.session_state.alarm_datetime = None

if "mode" not in st.session_state:
    st.session_state.mode = "기본 모드"

if "no_spray" not in st.session_state:
    st.session_state.no_spray = False

if "finished" not in st.session_state:
    st.session_state.finished = False

if "alarm_triggered_at" not in st.session_state:
    st.session_state.alarm_triggered_at = None

if not st.session_state.running and not st.session_state.finished:

    st.divider()
    st.subheader("⏰ 알람 설정")

    alarm_time = st.time_input(
        "기상 시간",
        value=time(7, 0),
        step=60
    )

    mode = st.radio(
        "작동 모드 선택",
        ["기본 모드", "특수 끼얹기 모드"]
    )

    no_spray = st.checkbox(
        "물을 뿌리지 않기",
        value=False
    )

    st.info(
        "기본 모드: 알람 후 15초 뒤 화면 효과\n\n"
        "특수 모드: 알람 시간에 즉시 화면 효과"
    )

    st.warning(
        "실제 액체는 분사하지 않습니다. "
        "화면 효과만 작동합니다."
    )

    if st.button("알람 시작", use_container_width=True):
        current = datetime.now(KST)

        alarm_dt = datetime.combine(
            current.date(),
            alarm_time,
            tzinfo=KST
        )

        if alarm_dt <= current:
            alarm_dt += timedelta(days=1)

        st.session_state.alarm_datetime = alarm_dt
        st.session_state.mode = mode
        st.session_state.no_spray = no_spray
        st.session_state.running = True
        st.session_state.finished = False
        st.session_state.alarm_triggered_at = None

        st.rerun()

elif st.session_state.running:

    @st.fragment(run_every="1s")
    def alarm_screen():
        now = datetime.now(KST)
        alarm_dt = st.session_state.alarm_datetime

        st.subheader("⏰ 알람 대기 중")
        st.write("설정된 알람:", alarm_dt.strftime("%Y-%m-%d %H:%M:%S"))
        st.write("현재 한국 시간:", now.strftime("%Y-%m-%d %H:%M:%S"))

        remaining = (alarm_dt - now).total_seconds()

        if remaining > 0:
            st.markdown(
                f"<h1 style='text-align:center;'>{int(remaining)}초</h1>",
                unsafe_allow_html=True
            )
            st.caption("알람 시간이 되면 작동합니다.")

        else:
            if st.session_state.alarm_triggered_at is None:
                st.session_state.alarm_triggered_at = now

            elapsed = (
                now - st.session_state.alarm_triggered_at
            ).total_seconds()

            should_finish = (
                st.session_state.mode == "특수 끼얹기 모드"
                or elapsed >= 15
            )

            if should_finish:
                st.session_state.running = False
                st.session_state.finished = True
                st.rerun()
            else:
                st.markdown(
                    "<h1 style='text-align:center;'>🔔 알람!</h1>",
                    unsafe_allow_html=True
                )
                st.write("15초 후 화면 효과가 시작됩니다.")

        if st.button("알람 취소", use_container_width=True):
            st.session_state.running = False
            st.session_state.alarm_datetime = None
            st.rerun()

    alarm_screen()

elif st.session_state.finished:

    st.title("💦 알람 종료!")

    if st.session_state.no_spray:
        st.success("물을 뿌리지 않도록 설정했습니다!")
        st.markdown(
            "<h1 style='text-align:center;'>🔔⏰</h1>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<div class='splash'>💦💧🌊</div>",
            unsafe_allow_html=True
        )
        st.success("기상 시간입니다!")

    st.warning(
        "주의: 이 앱은 실제 액체를 분사하지 않습니다. "
        "뜨거운 물이나 화학 물질 등 위험한 액체를 사용하지 마세요."
    )

    if st.button("처음으로 돌아가기", use_container_width=True):
        st.session_state.running = False
        st.session_state.finished = False
        st.session_state.alarm_datetime = None
        st.session_state.alarm_triggered_at = None
        st.rerun()
