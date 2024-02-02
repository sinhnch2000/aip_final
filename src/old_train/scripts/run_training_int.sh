export NCCL_DEBUG=INFO
WANDB_API_KEY=0b39e2667775768150d99b18418fb63ca15b13bc \
CUDA_VISIBLE_DEVICES=0,1 accelerate launch --config_file /kaggle/working/aip_final/src/old_train/config/config_fsdp_t5.yaml /kaggle/working/aip_final/src/old_train/train.py       \
        --module 'int' \
        --model_name "google/flan-t5-base" \
        --max_target_length 400 \
        --num_train_epochs 4 \
        --output_dir "./output/GradInt/0102"  \
        --train_files  "/kaggle/input/data-gradint/GradINT/FUSEDCHAT/train.json" "/kaggle/input/data-gradint/GradINT/SGD/train.json"\
        --val_files  "/kaggle/input/data-gradint/GradINT/FUSEDCHAT/val.json" "/kaggle/input/data-gradint/GradINT/SGD/train.json"\
        --resume_from_checkpoint "/kaggle/input/ckpt-int/epoch_2" \
        --batch_size  8 \
        --num_beams  4 \
        --weight_decay  0.3 \
        --learning_rate 1e-5 \
        --num_warmup_steps 100 \
        --gradient_accumulation_steps 16 \
        --with_tracking  \
        --report_to wandb \
        --checkpointing_steps epoch \
        --do_eval_per_epoch