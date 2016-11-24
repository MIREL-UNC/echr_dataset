echo "Training bag of word approach"
python bag_of_words.py --echr-dirpath /home/ccardellino/datasets/echr/samples_for_distances/ --wiki-filepath /home/ccardellino/datasets/echr/samples_for_distances/5000_wiki.txt --output_filename /home/ccardellino/datasets/echr/samples_for_distances/tsne_w2v_sentences.pickle --save_tsne --lr
echo "Training w2v with echr dataset"
python word_embeddings.py --echr-dirpath /home/ccardellino/datasets/echr/samples_for_distances/ --wiki-filepath /home/ccardellino/datasets/echr/samples_for_distances/5000_wiki.txt --output_filename /home/ccardellino/datasets/echr/samples_for_distances/tsne_w2v_echr_avg.pickle --save_tsne  --gensim_save --model_filepath /home/ccardellino/datasets/echr/wordvectors/100vectors.bin.gz --lr
echo "Training w2v with mixed dataset"
python word_embeddings.py --echr-dirpath /home/ccardellino/datasets/echr/samples_for_distances/ --wiki-filepath /home/ccardellino/datasets/echr/samples_for_distances/5000_wiki.txt --output_filename /home/ccardellino/datasets/echr/samples_for_distances/tsne_w2v_mixed_20Kwiki.pickle --save_tsne  --model_filepath /home/ccardellino/datasets/echr/wordvectors/100vectors_mixed_20Kwiki.bin.gz --lr
echo "Training w2v with wikipedia dataset"
python word_embeddings.py --echr-dirpath /home/ccardellino/datasets/echr/samples_for_distances/ --wiki-filepath /home/ccardellino/datasets/echr/samples_for_distances/5000_wiki.txt --output_filename /home/ccardellino/datasets/echr/samples_for_distances/tsne_w2v_wiki.pickle --save_tsne  --model_filepath /home/ccardellino/datasets/wordvectors/WikipediaEuroparlVectors.bin.gz --lr
