import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# 폰트 경로 (시스템에 NanumGothic이 없으면 설치 필요)
# Streamlit Cloud 배포 시에는 폰트 파일과 함께 배포해야 합니다.
# 폰트가 없는 경우, 주석 처리하거나 다른 폰트를 지정하세요.
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
행성이 렌즈 별 주위를 공전하며 **광원의 밝기 변화**에 어떻게 영향을 주는지 확인해 보세요.
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
    (이것은 실제 마이크로렌징 증폭 계산과 매우 다름. 개념적 시각화를 위함.)

    Args:
        source_position_relative (float): 렌즈 중심으로부터 광원의 상대적 위치.
        lens_positions (list of float): 각 렌즈의 상대적 위치.
        lens_masses (list of float): 각 렌즈의 질량.
        scale_factor (float): 증폭 효과의 스케일 조절.

    Returns:
        float: 밝기 증폭 값.
    """
    total_deflection_strength = 0
    for i in range(len(lens_positions)):
        distance = np.abs(source_position_relative - lens_positions[i])
        # 0으로 나누는 것을 방지
        if distance < 1e-6:
            distance = 1e-6
        total_deflection_strength += (lens_masses[i] / distance) * scale_factor

    # 밝기는 굴절 강도가 강할수록(가까울수록) 증가하도록 가정
    magnification = 1 + total_deflection_strength
    return magnification

# --- 시뮬레이션 실행 ---
# 시간 축 생성
times = np.linspace(-time_range / 2, time_range / 2, num_time_steps)

# 광원(배경 별)의 렌즈에 대한 상대적 위치 (시간에 따라 이동)
# 여기서는 광원이 렌즈 중심을 가로질러 이동한다고 가정
source_relative_positions = np.linspace(-min_approach_distance * 2, min_approach_distance * 2, num_time_steps)

# 행성의 궤도 계산 (렌즈 별 주위를 원형 궤도로 공전)
planet_x_orbit = orbit_radius * np.cos(times * np.pi / (time_range / 2)) # 행성 공전 시각화 (X축만 단순화)
planet_y_orbit = orbit_radius * np.sin(times * np.pi / (time_range / 2)) # 행성 공전 시각화 (Y축)

# 밝기 변화 저장 리스트
magnifications = []

for i, t in enumerate(times):
    # 각 시간 단계에서 렌즈 별과 행성의 위치
    current_star_pos = 0 # 렌즈 별은 중심에 고정
    current_planet_pos = planet_x_orbit[i] # 행성의 X 위치

    # 밝기 증폭 계산
    magnification = calculate_magnification(
        source_relative_positions[i],
        [current_star_pos, current_planet_pos],
        [star_mass, planet_mass]
    )
    magnifications.append(magnification)

# --- 시각화 ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("💡 밝기 변화 곡선 (Light Curve)")
    fig_lc, ax_lc = plt.subplots(figsize=(8, 4))
    ax_lc.plot(times, magnifications, color='darkorange', linewidth=2)
    ax_lc.set_xlabel("시간 (상대적)")
    ax_lc.set_ylabel("밝기 증폭 (상대적)")
    ax_lc.set_title("광원 별의 밝기 변화")
    ax_lc.grid(True)
    st.pyplot(fig_lc)

with col2:
    st.subheader("🔭 렌즈계와 광원의 움직임")
    fig_geo, ax_geo = plt.subplots(figsize=(8, 4))

    # 광원(배경 별)의 궤적
    ax_geo.plot(source_relative_positions, np.zeros_like(source_relative_positions), 'b--', alpha=0.5, label='광원 궤적')
    
    # 렌즈 별
    ax_geo.plot(0, 0, 'o', color='red', markersize=star_mass * 5, label=f'렌즈 별 (질량={star_mass:.1f})')
    
    # 행성의 궤적 (주변에 원형으로 그림)
    # 현재 시간에서의 행성 위치
    current_time_index = np.argmin(np.abs(times)) # 중간 시간 (0에 가까운)
    
    # 행성의 전체 궤도
    ax_geo.plot(planet_x_orbit, planet_y_orbit, 'g:', alpha=0.5, label='행성 궤도')
    
    # 현재 시점의 행성 위치 강조
    current_planet_x = planet_x_orbit[current_time_index]
    current_planet_y = planet_y_orbit[current_time_index]
    ax_geo.plot(current_planet_x, current_planet_y, 'o', color='green', markersize=planet_mass * 10 + 5, label=f'행성 (질량={planet_mass:.2f})')

    # 광원 현재 위치 (밝기 변화 그래프의 피크 지점)
    peak_index = np.argmax(magnifications)
    ax_geo.plot(source_relative_positions[peak_index], 0, 'P', color='blue', markersize=10, label='광원 (가장 밝을 때)')


    ax_geo.set_xlabel("상대 X 위치")
    ax_geo.set_ylabel("상대 Y 위치")
    ax_geo.set_title("렌즈계와 광원(가장 밝을 때)")
    ax_geo.set_xlim(-max(orbit_radius, min_approach_distance) * 2, max(orbit_radius, min_approach_distance) * 2)
    ax_geo.set_ylim(-max(orbit_radius, min_approach_distance) * 2, max(orbit_radius, min_approach_distance) * 2)
    ax_geo.set_aspect('equal', adjustable='box')
    ax_geo.grid(True)
    ax_geo.legend(loc='upper right', fontsize=8)
    st.pyplot(fig_geo)

st.markdown("""
---
### 시뮬레이션 해석
* **밝기 변화 곡선 (Light Curve):** 광원 별의 밝기가 시간에 따라 어떻게 변하는지 보여줍니다. 렌즈 별에 의해 광원 별이 지나갈 때 밝기가 크게 증폭됩니다.
* **행성의 영향:** 렌즈 별에 행성이 있다면, 이 행성이 광원의 경로에 놓일 때 주된 밝기 곡선에 **작은 봉우리(perturbation)**나 **골짜기(dip)**와 같은 추가적인 변화를 만듭니다. 이 미세한 변화가 바로 외계행성의 존재를 알려주는 중요한 단서입니다.
* **렌즈계와 광원의 움직임:** 이 그래프는 렌즈 별(붉은색), 행성(초록색), 그리고 광원 별(파란색 점선 궤적)의 상대적인 위치를 보여줍니다. 광원 별이 렌즈 별과 행성 주위를 지날 때 밝기가 증폭됩니다.

**참고:** 이 시뮬레이션은 미세 중력렌즈 현상을 **개념적으로 이해**하기 위한 **매우 단순화된 모델**입니다. 실제 미세 중력렌즈 현상은 복잡한 일반 상대성 이론과 천체역학을 바탕으로 계산되며, 밝기 곡선 또한 훨씬 복잡한 형태를 띱니다.
""")
