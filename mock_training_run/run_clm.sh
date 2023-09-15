python mock_training_run/run_clm.py \
    --model_name_or_path HuggingFaceH4/tiny-random-LlamaForCausalLM \
    --dataset_name manu/french_open_subtitles \
    --gradient_accumulation_steps 8 \
    --per_device_train_batch_size 2 \
    --per_device_eval_batch_size 8 \
    --do_train \
    --do_eval \
    --output_dir ./data/test-clm \
    --report_to tensorboard \
    --logging_steps 100 \
    --save_total_limit 3 \
    # --streaming \
