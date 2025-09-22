# Weather Effect Generator 使用指南

## 项目概述

本项目实现了基于神经场的多物理场扰动建模与可微渲染系统，能够将普通图像转化为复杂天气下的场景。项目包含以下核心功能：

1. **多物理场扰动建模**：实现湿度场、散射系数场、风速场、温度场的神经建模
2. **可微渲染系统**：基于体积渲染方程的物理一致性图像生成
3. **物理约束优化**：空间平滑性、质量守恒、热力耦合等物理约束

## 快速开始

### 1. 安装依赖

```bash
# 安装基础依赖
pip install -r simple_requirements.txt

# 或者手动安装
pip install torch numpy Pillow matplotlib
```

### 2. 运行演示

#### 使用演示数据（推荐）

```bash
# 生成所有天气效果
python simple_weather_demo.py --use_demo --weather_type all

# 生成特定天气效果
python simple_weather_demo.py --use_demo --weather_type fog --intensity 0.7
python simple_weather_demo.py --use_demo --weather_type rain --intensity 0.8
python simple_weather_demo.py --use_demo --weather_type snow --intensity 0.6
```

#### 使用自己的图像

```bash
# 使用自己的图像和深度图
python simple_weather_demo.py --input_image your_image.jpg --depth_map your_depth.npy --weather_type fog

# 只提供图像，自动生成深度图
python simple_weather_demo.py --input_image your_image.jpg --weather_type all
```

### 3. 参数说明

- `--input_image`: 输入图像路径
- `--depth_map`: 深度图路径（.npy格式）
- `--output_dir`: 输出目录（默认：weather_results）
- `--weather_type`: 天气类型（fog/rain/snow/all）
- `--intensity`: 天气强度（0.0-1.0）
- `--use_demo`: 使用内置演示数据

## 输出结果

运行后会在输出目录中生成：

1. **单独天气效果图像**：如 `fog_0.6.jpg`, `rain_0.8.jpg` 等
2. **对比图**：`weather_comparison.png` - 显示原始图像和所有天气效果的对比
3. **演示数据**：`demo_original.jpg`, `demo_depth.npy`（如果使用演示数据）

## 高级功能

### 1. 神经场天气生成器

```python
from neural_weather_generator import NeuralWeatherGenerator

# 创建生成器
generator = NeuralWeatherGenerator()

# 生成天气效果
weather_image = generator.generate_weather_effect(
    image, depth, weather_type='fog', intensity=0.5
)
```

### 2. 增强版生成器

```python
from enhanced_weather_generator import EnhancedWeatherGenerator

# 创建增强版生成器
generator = EnhancedWeatherGenerator(use_neural_field=True)

# 使用不同方法生成
# traditional: 传统分析方法
# neural: 神经场方法
# hybrid: 混合方法
weather_image = generator.generate_weather_effect(
    image, depth, weather_type='fog', intensity=0.5, method='hybrid'
)
```

### 3. 物理一致性评估

```python
# 评估物理一致性
metrics = generator.evaluate_physics_consistency(image, depth, 'fog')
print("物理一致性指标:", metrics)
```

## 天气类型说明

### 雾效果 (Fog)
- **物理机制**：湿度场影响能见度，散射系数影响光照衰减
- **视觉效果**：降低对比度，增加白色雾气
- **参数调节**：强度越高，雾气越浓，能见度越低

### 雨效果 (Rain)
- **物理机制**：结合雾效果和雨滴散射
- **视觉效果**：雾化背景 + 雨滴纹理
- **参数调节**：强度影响雨滴密度和雾气浓度

### 雪效果 (Snow)
- **物理机制**：结合雾效果和雪花散射
- **视觉效果**：雾化背景 + 白色雪花
- **参数调节**：强度影响雪花密度和雾气浓度

## 技术架构

### 核心组件

1. **NeuralWeatherField**: 四分支神经场，建模四个物理变量
2. **PhysicsRegularizer**: 物理一致性正则化器
3. **DifferentiableRenderer**: 可微体积渲染器
4. **EnhancedWeatherGenerator**: 集成传统和神经方法的生成器

### 物理建模

- **湿度场 μ(x,y,z)**: 决定局部云雾凝结趋势
- **散射系数场 σ_s(x,y,z)**: 反映粒子分布对光照的衰减
- **风速场 v⃗(x,y,z)**: 控制湿度场的空间对流
- **温度场 T(x,y,z)**: 调控湿度-散射的相变机制

### 约束条件

- **空间平滑性**: 防止扰动场剧烈跳变
- **质量守恒**: 风速场满足无源特性
- **热力耦合**: 温度梯度与风速的线性耦合

## 故障排除

### 常见问题

1. **依赖安装失败**
   ```bash
   # 尝试使用国内镜像
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple torch numpy Pillow matplotlib
   ```

2. **CUDA不可用**
   - 脚本会自动检测并使用CPU
   - 确保安装了正确版本的PyTorch

3. **内存不足**
   - 减小图像尺寸
   - 使用较小的神经场模型

### 性能优化

- 使用GPU加速（如果可用）
- 调整神经场层数和隐藏维度
- 使用批量处理进行大规模生成

## 论文对应

本项目实现了论文中描述的以下内容：

- **3.1 多物理场扰动建模**
  - 3.1.1 天气生成的物理形式化
  - 3.1.2 神经建模方式：四分支轻量级神经场结构
  - 3.1.3 扰动空间连续性与物理一致性的联合约束

- **3.2 扰动场至图像的可微渲染建模**
  - 3.2.1 前向图像生成机制：物理一致性的可微渲染过程
  - 3.2.2 反向优化通路建构：感知误差驱动的梯度传播路径
  - 3.2.3 系统实现机制：可导链路、稳定训练与跨平台复现保障

## 联系方式

如有问题或建议，请通过以下方式联系：
- 项目地址：[GitHub Repository]
- 邮箱：[Your Email] 