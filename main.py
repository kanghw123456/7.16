import numpy as np
import matplotlib.pyplot as plt

def gravitational_lens_deflection(source_x, source_y, lens_mass, lens_x=0, lens_y=0, scale=1):
    """
    중력 렌즈에 의한 빛의 굴절을 계산합니다.
    (이것은 단순화된 모델이며, 실제 중력 렌즈 방정식과는 다릅니다.)

    Args:
        source_x (float or np.array): 광원의 X 좌표.
        source_y (float or np.array): 광원의 Y 좌표.
        lens_mass (float): 렌즈의 질량 (상대적인 값).
        lens_x (float): 렌즈의 X 좌표.
        lens_y (float): 렌즈의 Y 좌표.
        scale (float): 굴절 효과의 스케일 조절.

    Returns:
        tuple: 굴절된 광원의 (X, Y) 좌표.
    """
    dx = source_x - lens_x
    dy = source_y - lens_y
    r_squared = dx**2 + dy**2
    
    # 0으로 나누는 것을 방지
    r_squared[r_squared == 0] = 1e-9 

    # 굴절 각도 (간단한 반비례 모델)
    alpha = (lens_mass / r_squared) * scale

    # 굴절 방향 벡터 (렌즈 중심으로 향하는 벡터의 반대)
    nx = -dx / np.sqrt(r_squared)
    ny = -dy / np.sqrt(r_squared)

    # 굴절된 위치 계산 (원래 위치 + 굴절 방향 * 굴절 각도)
    deflected_x = source_x + nx * alpha
    deflected_y = source_y + ny * alpha
    
    return deflected_x, deflected_y

# --- 시뮬레이션 설정 ---
# 배경 은하 (광원)의 초기 위치
num_sources = 500
np.random.seed(42) # 재현성을 위해 시드 설정
source_xs_original = np.random.uniform(-5, 5, num_sources)
source_ys_original = np.random.uniform(-5, 5, num_sources)

# 렌즈 은하의 설정
lens_mass = 100 # 렌즈의 상대적인 질량
lens_x_pos = 0   # 렌즈의 X 좌표
lens_y_pos = 0   # 렌즈의 Y 좌표

# 굴절 효과 스케일
deflection_scale = 0.5

# --- 굴절된 광원 위치 계산 ---
deflected_xs, deflected_ys = gravitational_lens_deflection(
    source_xs_original, source_ys_original, lens_mass, 
    lens_x=lens_x_pos, lens_y=lens_y_pos, scale=deflection_scale
)

# --- 시각화 ---
plt.figure(figsize=(12, 6))

# 1. 렌즈가 없을 때 (원본)
plt.subplot(1, 2, 1)
plt.scatter(source_xs_original, source_ys_original, s=5, alpha=0.7, color='blue')
plt.scatter(lens_x_pos, lens_y_pos, s=200, marker='o', color='red', label='Lens Galaxy')
plt.title('Original Background Galaxy (No Lens)')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.grid(True)
plt.axvline(0, color='gray', linestyle='--', linewidth=0.5)
plt.axhline(0, color='gray', linestyle='--', linewidth=0.5)
plt.xlim([-7, 7])
plt.ylim([-7, 7])
plt.legend()
plt.gca().set_aspect('equal', adjustable='box')


# 2. 렌즈가 있을 때 (굴절 후)
plt.subplot(1, 2, 2)
plt.scatter(deflected_xs, deflected_ys, s=5, alpha=0.7, color='purple')
plt.scatter(lens_x_pos, lens_y_pos, s=200, marker='o', color='red', label='Lens Galaxy')
plt.title('Gravitational Lensing Effect')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.grid(True)
plt.axvline(0, color='gray', linestyle='--', linewidth=0.5)
plt.axhline(0, color='gray', linestyle='--', linewidth=0.5)
plt.xlim([-7, 7])
plt.ylim([-7, 7])
plt.legend()
plt.gca().set_aspect('equal', adjustable='box')

plt.tight_layout()
plt.show()
