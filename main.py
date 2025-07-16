import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# 폰트 경로 (시스템에 NanumGothic이 없으면 설치 필요)
font_path = "NanumGothic.ttf"
if os.path.exists(font_path):
    try:
        fm.fontManager.addfont(font_path)
        plt.rc('font', family='NanumGothic')
        plt.rcParams['axes.unicode_minus'] = False
    except Exception as e:
        st.warning(f"⚠️ 폰트 적용 실패: {e}. 기본 폰트로 표시됩니다.")
else:
    st.warning("⚠️ 'NanumGothic.ttf' 폰트 파일을 찾을 수 없습니다. 기본 폰트로 표시됩니다.")

st.title("🌌 외계행성 미세 중력렌즈 시뮬레이션")

st.markdown("""
멀리 있는 별빛이 우리 시선에 놓인 다른 별과 그 주위를 도는 행성에 의해
잠시 밝아지는 **미세 중력렌즈** 현상을 시뮬레이션해 보세요!
**아래 시간 슬라이더를 움직여 각 시점에서 별과 행성, 광원의 위치가 어떻게 변하는지 확인해 보세요.**
""")

st.sidebar.header("시뮬레이션 설정")

# --- 설정 변수 ---
# 렌즈 별의 질량 (상대적 값)
star_mass = st.sidebar.slider("렌즈 별의 질량 (상대값)", 1.0, 10.0, 5.0, 0.1)

# 행성의 질량 (렌즈 별 질량에 대한 비율)
planet_mass_ratio = st.sidebar.slider("행성의 질량 (렌즈 별 질량에 대한 비율)", 0.01, 1.0, 0.1, 0.01)
planet_mass = star_mass * planet_mass_ratio

# 행성의 궤도 반지름 (렌즈 별 주위)
orbit_radius = st.sidebar.slider("행성 궤도 반지름 (AU)", 0.1, 2.0, 0.5, 0.05)

# 광원(배경 별)의 최소 접근 거리 (렌즈로부터)
min_approach_distance = st.sidebar.slider("광원의 최소 접근 거리 (렌즈 중심으로부터)", 0.1, 2.0, 0.5, 0.1)

# 시뮬레이션 시간 범위 (상대적)
time_range = st.sidebar.slider("시뮬레이션 시간 범위 (상대적)", 5, 50, 20)

# 시간 단계 수
num_time_steps = st.sidebar.slider("시뮬레이션 시간 단계 수", 50, 500, 200)

st.sidebar.markdown("---")
st.sidebar.info("""
**설명:**
- **렌즈 별:** 우리 시선에 놓여 광원 별빛을 휘게 하는 주된 질량체.
- **행성:** 렌즈 별 주위를 공전하며 밝기 변화에 미세한 이상 현상(anomaly)을 만듭니다.
- **광원의 최소 접근 거리:** 광원이 렌즈에 가장 가까이 다가오는 가상의 거리입니다.
""")

# --- 중력렌즈 밝기 계산 함수 ---
# (매우 단순화된 모델. 실제는 복잡한 마이크로렌징 방정식을 사용합니다.)
def calculate_magnification(source_position_relative, lens_positions, lens_masses, scale_factor=0.1):
    """
    주어진 광원 위치와 렌즈 정보에 따른 대략적인 밝기 증폭을 계산합니다.
    (이것은 실제 마이크로렌딩 증폭 계산과 매우 다름. 개념적 시각화를 위함.)

    Args:
        source_position_relative (float or np.array): 렌즈 중심으로부터 광원의 상대적 위치.
        lens_positions (list of float or np.array): 각 렌즈의 상대적 X, Y 위치.
        lens_masses (list of float): 각 렌즈의 질량.
        scale_factor (float): 증폭 효과의 스케일 조절.

    Returns:
        float or np.array: 밝기 증폭 값.
    """
    total_def
