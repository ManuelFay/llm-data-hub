python mock_training_run/run_clm.py \
    --config_name mock_training_run/llama_configs/config.json \
    --tokenizer_name "manu/tok-fr-en-code" \
    --dataset_name open-phi/textbooks \
    --gradient_accumulation_steps 2 \
    --per_device_train_batch_size 2 \
    --per_device_eval_batch_size 2 \
    --do_train \
    --do_eval \
    --max_steps 10000 \
    --warmup_steps 1000 \
    --output_dir ./data/test-clm \
    --report_to tensorboard \
    --logging_steps 100 \
    --save_total_limit 3 \
    --push_to_hub \
    --push_to_hub_model_id "test-clm"
    # --streaming \


#    --dataset_name wikipedia     --dataset_config_name 20220301.fr \
# sbatch --job-name=mdeb --nodes=1 --time=24:00:00 -p gpua100 --cpus-per-task 32 --gres=gpu:4 --error=data/log.err \
#        --output=data/log.out --wrap="deepspeed --num_gpus=4  mock_training_run/run_clm.py \
#                                                 --config_name mock_training_run/llama_configs/config.json \
#                                                 --tokenizer_name manu/tok-fr-en-code \
#                                                 --dataset_name wikipedia \                                                                                                                                                                             --dataset_config_name 20220301.fr \
#                                                 --gradient_accumulation_steps 8 \
#                                                 --per_device_train_batch_size 16 \
#                                                 --per_device_eval_batch_size 16 \
#                                                 --do_train \
#                                                 --do_eval \
#                                                 --output_dir ./data/test-clm \
#                                                 --report_to tensorboard \
#                                                 --logging_steps 100 \
#                                                 --save_total_limit 3 \
#                                                 --push_to_hub \
#                                                 --push_to_hub_model_id manu/test-clm"