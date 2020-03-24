1. full images, rescaled to 512//4, 384//4, 1 epoch frozen https://ui.neptune.ai/o/appsilon/org/gabon-wildlife/e/GAB-1/charts
   * val_loss = 1.63
   * acc = 0.53

2. (continued training from 1.) full images, rescaled to 512//4, 384//4, 5 epochs unfrozen https://ui.neptune.ai/o/appsilon/org/gabon-wildlife/e/GAB-3/charts
overfitting, but beginning is decent.
   * val_loss = 1.60 -> 1.83
   * acc = 0.54 -> 0.56

3. stage1 - rescaled images, rescaled to 512//4, 384//4, 1 epochs, frozen /training/training_04_rescaled_stage1.ipynb
   * val_loss = 2.07
   * acc = 0.43 

4. (continue form 3.) rescaled images, rescaled to 512//4, 384//4, 3epochs unfrozen woven-pyramid-4 (training_05_rescaled_wandb.ipynb)
   * val_loss = 1.72 -> 1.76
   * acc = 0.53 -> 0.55

5. stage2 - (continue form 3.) rescaled images, rescaled to 512//4, 384//4, 6epochs unfrozen genial-deluge-6 (training_06_rescaled_wandb_longer.ipynb)
   * val_loss = 1.84 -> 1.78 (in 4epoch), later higher
   * acc = 0.50 -> 0.56 (in 4epoch), later similar

6. stage3 - (continue from best model in 5.) rescaled images, rescaled to 512//2, 384//2, 1epochs frozen valiant-music-9 training_07_rescaled_wandb_by2.ipynb
   * val_loss = 1.46
   * acc =  0.60

7. stage4 - (continue from model in 6.) rescaled images, rescaled to 512//2, 384//2, 5epochs unfrozen fallen-terrain-10 training_08_rescaled_wandb_by2.ipynb
   * val_loss = 1.30
   * acc =  0.65

8. stage5 - (continue from model in 7.) rescaled images, 2epochs frozen ethereal-fire-12 training_09_rescaled_wandb_full.ipynb
   * val_loss = 1.13
   * acc =  0.69

9. stage6 - (continue from model in 8.) rescaled images, 5epochs unfrozen effortless-morning-14 training_10_rescaled_wandb_full.ipynb
   * val_loss = 0.98
   * acc =  0.75

10. stage1a - (from scratch) rescaled images, 5epochs frozen autumn-bee-16 (wysypało się po 3epokach) radiant-star-18 training_11_rescaled_wandb_full.ipynb
   * val_loss = 1.01
   * acc =  0.72

11. stage2a - (from model in 10.) rescaled images, 5epochs unfrozen [noble-water-21](https://app.wandb.ai/jedrzej/gabon/runs/19wnwr2w) (best model after 3) training_12_rescaled_wandb_full.ipynb
   * val_loss = 0.85
   * acc = 0.77

12. stage3a - (from model in 11.) full images, but 1,5x of rescaled in each dim (so 576x~768), 5epochs frozen sweet-potato-flan-25 (broke after 3 epochs) training_13_wandb_full_from_scratch_bigger_images.ipynb
   * val_loss = 0.84
   * acc = 0.77

13. stage4a - (from model in 12.) full images, but 1,5x of rescaled in each dim (so 576x~768), 5epochs unfrozen [fluent-brook-27](https://app.wandb.ai/jedrzej/gabon/runs/yhcil4dn) (broke after 4 epochs) training_14_wandb_full_from_scratch_bigger_images.ipynb (best model: stage4a-intermediate_bestmodel.pth)
   * val_loss = 0.72
   * acc = 0.80
