python mock_training_run/run_clm.py \
    --config_name llama_configs/config.json \
    --tokenizer_name "manu/tok-fr-en-code" \
    --dataset_name manu/french-30b \
    --gradient_accumulation_steps 8 \
    --per_device_train_batch_size 16 \
    --per_device_eval_batch_size 16 \
    --do_train \
    --do_eval \
    --output_dir ./data/test-clm \
    --report_to tensorboard \
    --logging_steps 100 \
    --save_total_limit 3 \
    --push_to_hub \
    --push_to_hub_model_id "manu/test-clm" \
    # --streaming \
