python mock_training_run/run_mlm.py \
    --model_name_or_path microsoft/deberta-v3-xsmall \
    --dataset_name manu/french_open_subtitles \
    --per_device_train_batch_size 8 \
    --per_device_eval_batch_size 8 \
    --do_train \
    --do_eval \
    --output_dir ./data/test-mlm \
    --report_to tensorboard \
    --logging_steps 100 \
    --save_total_limit 3 \
    # --streaming