python mock_training_run/run_clm.py \
    --config_name mock_training_run/llama_configs/config_small.json \
    --tokenizer_name "manu/tok-fr-en-code" \
    --dataset_name manu/illuin_layout_dataset_text_only \
    --gradient_accumulation_steps 8 \
    --per_device_train_batch_size 1 \
    --per_device_eval_batch_size 1 \
    --do_train \
    --do_eval false \
    --max_steps 10000 \
    --block_size 256 \
    --warmup_steps 1000 \
    --output_dir ./data/test-clm \
    --report_to tensorboard \
    --logging_steps 100 \
    --save_total_limit 3 \
    --push_to_hub \
    --push_to_hub_model_id "test-clm-small" \
    --overwrite_output_dir \
    --fp16 \
    # --streaming \


 sbatch --job-name=mdeb --nodes=1 --time=24:00:00 -p gpua100 --cpus-per-task 32 --gres=gpu:4 --error=data/log.err \
        --output=data/log.out --wrap="accelerate launch mock_training_run/run_clm.py \
                                                 --config_name mock_training_run/llama_configs/config.json \
                                                 --tokenizer_name manu/tok-fr-en-code \
                                                 --dataset_name  wikitext --dataset_config_name wikitext-103-v1 \
                                                 --gradient_accumulation_steps 32 \
                                                 --per_device_train_batch_size 4 \
                                                 --per_device_eval_batch_size 8 \
                                                 --preprocessing_num_workers 32 \
                                                 --num_train_epochs 3 --warmup_ratio 0.05 \
                                                 --learning_rate 3e-4 \
                                                 --block_size 2048 \
                                                 --do_train \
                                                 --do_eval false \
                                                 --bf16 \
                                                 --output_dir ./data/llama-wikitext \
                                                 --report_to tensorboard \
                                                 --logging_steps 10 --save_steps 100 --eval_steps 100 \
                                                 --save_total_limit 3 \
                                                 --push_to_hub \
                                                 --overwrite_output_dir \
                                                 --torch_compile \
                                                 --ddp_find_unused_parameters false \
                                                 --hub_model_id manu/llama-wikitext"

 sbatch --job-name=mdeb --nodes=1 --time=24:00:00 -p gpua100 --cpus-per-task 32 --gres=gpu:4 --error=data/log.err \
        --output=data/log.out --wrap="accelerate launch mock_training_run/run_clm.py \
                                                 --config_name mock_training_run/llama_configs/config.json \
                                                 --tokenizer_name manu/tok-fr-en-code \
                                                 --dataset_name  oscar-corpus/OSCAR-2301 --dataset_config_name fr --streaming \
                                                 --gradient_accumulation_steps 32 \
                                                 --per_device_train_batch_size 4 \
                                                 --per_device_eval_batch_size 8 \
                                                 --preprocessing_num_workers 32 \
                                                 --max_steps 10000 --warmup_steps 500 \
                                                 --learning_rate 3e-4 \
                                                 --block_size 2048 \
                                                 --do_train \
                                                 --do_eval false \
                                                 --bf16 \
                                                 --output_dir ./data/llama-oscar-fr \
                                                 --report_to tensorboard \
                                                 --logging_steps 10 --save_steps 100 --eval_steps 100 \
                                                 --save_total_limit 3 \
                                                 --push_to_hub \
                                                 --overwrite_output_dir \
                                                 --torch_compile \
                                                 --ddp_find_unused_parameters false \
                                                 --hub_model_id manu/llama-oscar-fr"

# --max_steps 100000 --warmup_steps 1000 \