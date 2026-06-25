本页面介绍训练选项卡上的自定义调度器功能。此选项允许您使用 OneTrainer 中当前没有但可能存在于其他地方的调度器，例如在 PyTorch 中。如果您对 OneCycle 感兴趣，那么这就是允许您实现它的功能

如果读完后您仍然不确定，那么不要使用自定义调度器。这是一个面向高级用户的功能。

# 选择

为了使用自定义调度器，您需要在训练选项卡上选择它。

![image](https://github.com/Nerogar/OneTrainer/assets/132208482/1e5d02c2-e629-4dec-b883-aa344c464f7f)


# 配置

为了实际定义自定义调度器，您需要点击三个点（...），这将打开自定义调度器窗口。

![image](https://github.com/Nerogar/OneTrainer/assets/132208482/3d465c19-a42c-4c66-b683-464cb169c737)

## 设置

在此窗口上，通常会向您展示一个空白模板，您需要填写信息以使用您选择的自定义调度器。如果您将鼠标悬停在大多数字段上，会有工具提示。

* 类名（默认：空白）- 这是您定义要使用的调度器的模块和类名的地方。在此示例中，它是 torch.optim.lr_scheduler.MultiStepLR
* 添加参数 - 此按钮将添加两个空白字段。参数名称，以及您的自定义调度器正在寻找的值。有一些 OneTrainer 变量可以向前传递，工具提示会显示。

在上面的示例中，两个参数被传递给自定义调度器 MultiStepLR。第一个是里程碑，值为 50,100,150，gamma 为 .5。在此示例中，自定义调度器将在 50、100 和 150 步（如果您使用预热，则在预热完成后）将学习率降低 0.5。
这将为关键调优创建以下 LR 作为示例。

| 步骤 | LoRA Unet LR | 嵌入 LR |
|------|--------------|---------------|
| 0    | 1e-4         | 1e-3          |
| 50   | 5e-5         | 5e-4          |
| 100  | 2.5e-5       | 2.5e-4        |
| 150+ | 1.25e-5      | 1.25e-4       |

# 自定义调度器

PyTorch 包含 OneTrainer 中不标准包含的自定义调度器。它们可以在这里找到：(https://pytorch.org/docs/stable/optim.html#how-to-adjust-learning-rate)

这里列出的每个调度器都会列出它正在寻找的名称和参数。

一些示例：
* 多步线性：https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.MultiStepLR.html#torch.optim.lr_scheduler.MultiStepLR
* OneCycle：https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.OneCycleLR.html#torch.optim.lr_scheduler.OneCycleLR

# 示例
### 余弦退火
一个周期（意味着它会重复），您可以控制余弦的步数和最小 LR。普通余弦调度器将以接近 0 的学习率结束，而此自定义余弦可以以您控制的学习率值结束。这是一个冷周期，因为学习率将在下一个周期开始时逐渐增加（与热重启相比）。

* 类名：`torch.optim.lr_scheduler.CosineAnnealingLR`
* 参数：`T_max` 这设置周期的步数。如果此值不等于 OneTrainer 值，余弦将再次开始增加。
* 参数：`eta_min` 这设置余弦的最小学习率。例如，使用 5e-5 的值将使余弦在此值而不是 0 处触底。

### OneCycle
一个周期（意味着它会重复），缓慢预热到峰值，然后向最终值下降。OneCycle 有许多可以调整的参数，但这将专注于基本参数，设置长度和学习率的值。

* 类名：`torch.optim.lr_scheduler.OneCycleLR`
* 参数：`max_lr` 这设置 OneCycle 的峰值。例如，3e-4 的值将把峰值 LR 设置为此值。默认情况下，此值在您步数的 30% 处达到。（您需要将其提供给 OneCycle，它不会使用 OneTrainer 的 LR）
* 参数：`div_factor` 此参数使用公式 initial_lr = max_lr/div_factor 设置周期的初始学习率。在上面的示例中，使用 25 的 div_factor 将把初始 LR 设置为 1.2e-5。
* 参数：`final_div_factor` 此参数使用公式 min_lr = initial_lr/final_div_factor 设置周期的最终学习率。在上面的示例中，使用 .2（2e-1）的 final_div_factor 将把 min_lr 设置为 6e-5。
* 参数：`total_steps` 此参数设置周期中的步数。如果此值不等于 OneTrainer 值，周期将重复，或提前结束。


# 额外阅读
Medium 上有各种关于调度器的文章，包括 OneCycle，但有些在付费墙后面。

此页面深入介绍了 OneCycle：https://www.deepspeed.ai/tutorials/one-cycle/

此图像显示了 PyTorch 中每个调度器的图形外观：
![image](https://github.com/Nerogar/OneTrainer/assets/132208482/62788047-0fff-4d05-a95e-432e615d6947)
