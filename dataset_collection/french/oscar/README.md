---
license: cc0-1.0
size_categories:
- n>1T
multilinguality:
- multilingual
source_datasets:
- original
task_categories:
- fill-mask
- text-generation
task_ids:
- language-modeling
paperswithcode_id: oscar
extra_gated_prompt: "By filling the form below, you understand that only the metadata and the annotations of OSCAR 23.01 have a cc0-1.0 license, and that the rest of the content is crawled data derived from the November/December 2022 snapshot of Common Crawl, for which the authors of OSCAR **do not** hold any copyright whatsoever."
extra_gated_fields:
 Name: text
 Email: text
 Affiliation: text
 Country: text
 Usecase: text
 I have explicitly check with my jurisdiction and I confirm that downloading OSCAR 2301 is legal in the country/region where I am located right now, and for the use case that I have described above: checkbox
---

# Dataset Card for "OSCAR 23.01"

## IMPORTANT NOTE: THIS DATASET CARD IS STILL BEING WRITTEN, PLEASE BE PATIENT WHILE WE COMPLETE ALL THE INFORMATION ABOUT THE CORPUS

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits)
- [Dataset Creation](#dataset-creation)
  - [Curation Rationale](#curation-rationale)
  - [Source Data](#source-data)
  - [Annotations](#annotations)
  - [Personal and Sensitive Information](#personal-and-sensitive-information)
- [Considerations for Using the Data](#considerations-for-using-the-data)
  - [Social Impact of Dataset](#social-impact-of-dataset)
  - [Discussion of Biases](#discussion-of-biases)
  - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** [https://oscar-project.org](https://oscar-project.org)
- **Repository:** [https://github.com/oscar-project](https://github.com/oscar-project)
- **Papers:** [Towards a Cleaner Document-Oriented Multilingual Crawled Corpus](https://aclanthology.org/2022.lrec-1.463/), [Perplexed by Quality: A Perplexity-based Method for Adult and Harmful Content Detection in Multilingual Heterogeneous Web Data](https://arxiv.org/abs/2212.10440)
- **Point of Contact:** [Contact](https://oscar-project.org/#contact)

### Dataset Summary

The OSCAR project (**O**pen **S**uper-large **C**rawled **A**ggregated co**R**pus) is an Open Source project aiming to provide web-based multilingual resources and datasets for Machine Learning (ML) and Artificial Intelligence (AI) applications. The project focuses specifically in providing large quantities of unannotated raw data that is commonly used in the pre-training of large deep learning models. The OSCAR project has developed [high-performance data pipelines](https://github.com/oscar-corpus/ungoliant) specifically conceived to classify and filter large amounts of [web data](https://commoncrawl.org/). The project has also put special attention in improving the data quality of web-based corpora as well as providing data for low-resource languages, so that these new ML/AI technologies are accessible to as many communities as possible.

OSCAR 23.01 is the January 2023 version of the OSCAR Corpus based on the [November/December 2022 dump of Common Crawl](https://commoncrawl.org/2022/12/nov-dec-2022-crawl-archive-now-available/). While being quite similar to OSCAR 22.01, it contains several new features, including [KenLM](https://kheafield.com/code/kenlm/)-based adult content detection, precomputed [Locality-Sensitive Hashes](https://fr.wikipedia.org/wiki/Locality_sensitive_hashing) for near deduplication, and [blocklist](https://dsi.ut-capitole.fr/blacklists/index_en.php)-based categories. OSCAR 23.01 has also moved from gzip to [Zstandard compression](https://facebook.github.io/zstd/). You might already have `zstd` installed on your system, but if not, please check the [Zstandard website](https://facebook.github.io/zstd/) for installation instructions.

### Supported Tasks and Leaderboards

OSCAR is mainly intended to pretrain language models and word representations.

### Languages

All the data is distributed by language, both the original and the deduplicated versions of the data are available. 151 different languages are available. The table in subsection [Data Splits Sample Size](#data-splits-sample-size) provides the language code for each subcorpus as well as the number of words (space separated tokens), lines and sizes for both the original and the deduplicated versions of OSCAR.

### Issues

OSCAR 23.01 may have quality issues on low size subcorpora, as it has been the case before.

Note that since the documents are identified as a whole, it is expected to have lines in other languages in a given language subcorpus.
As an example, it is known and expected that the German subcorpus contains documents holding lines identified as Swiss German / Alemannic.

**If you encounter something that is unexpected, please file an issue here: https://github.com/oscar-corpus/corpus/issues.**

|Language code|Language|Issues|
|-------------|--------|------|
|             |        |      |
## Dataset Structure

We show detailed information for all the configurations of the dataset.

### Data Instances

TODO

### Layout

```js
{
   "content":"English sentence\nphrase en français\n????????????", // (1)
   "warc_headers":{ // (2)
      "warc-identified-content-language":"fra,eng",
      "warc-target-uri":"https://fr.wikipedia.org/wiki/...",
      "warc-record-id":"<urn:uuid:29eaa920-d299-4b1d-b687-c72bd8d68116>",
      "warc-type":"conversion",
      "content-length":"35298", // (3)
      "warc-refers-to":"<urn:uuid:39e42055-0d94-4e45-9c6c-9e7056635d64>",
      "warc-block-digest":"sha1:WFH2A5WHCS2H365GIAFYQPI7UOAMFGHB", // (3)
      "warc-date":"2022-11-26T09:45:47Z",
      "content-type":"text/plain"
   },
   "metadata":{
      "identification":{ // (4)
         "label":"fr",
         "prob":0.8938327
      },
      "harmful_pp":4063.1814, // (5)
      "tlsh":"tlsh:T125315FF2B6088901EEA097015DB39B4600B...", // (6)
      "quality_warnings":[ // (7)
         "short_sentences",
         "header",
         "footer"
      ],
      "categories":[ // (8)
         "examen_pix",
         "liste_bu"
      ],
      "sentence_identifications":[ // (9)
         {
            "label":"fr",
            "prob":0.99837273
         },
         {
            "label":"en",
            "prob":0.9992377
         },
         null
      ]
   }
}
```

### Data Splits


<details>
  <summary>Click to expand the number of samples per configuration</summary>
</details>

## Table

|     | Code   | Language                 | # docs        | # words         | Content Length :  |
|----:|:-------|:-------------------------|:--------------|:----------------|:-----------------|
|   0 | af     | Afrikaans                | 23,994        | 6,217,024       | 37.2 MB          |
|   1 | sq     | Albanian                 | 1,342,790     | 462,694,599     | 3.2 GB           |
|   2 | am     | Amharic                  | 119,434       | 40,262,809      | 512.9 MB         |
|   3 | ar     | Arabic                   | 25,012,116    | 10,081,452,882  | 110.7 GB         |
|   4 | an     | Aragonese                | 34            | 264             | 11.0 kB          |
|   5 | hy     | Armenian                 | 1,056,974     | 336,045,041     | 4.9 GB           |
|   6 | as     | Assamese                 | 89,542        | 24,395,215      | 412.1 MB         |
|   7 | ast    | Asturian                 | 440           | 10,917          | 74.1 kB          |
|   8 | av     | Avaric                   | 44            | 1,073           | 18.6 kB          |
|   9 | az     | Azerbaijani              | 1,159,994     | 316,850,330     | 3.0 GB           |
|  10 | bn     | Bangla                   | 3,474,086     | 1,092,983,765   | 19.1 GB          |
|  11 | ba     | Bashkir                  | 128,248       | 26,036,637      | 363.7 MB         |
|  12 | eu     | Basque                   | 678,474       | 136,672,615     | 1.2 GB           |
|  13 | be     | Belarusian               | 445,612       | 164,729,607     | 2.3 GB           |
|  14 | bh     | Bihari languages         | 48            | 507             | 6.8 kB           |
|  15 | bpy    | Bishnupriya              | 2,346         | 346,947         | 5.4 MB           |
|  16 | bs     | Bosnian                  | 20            | 395             | 3.0 kB           |
|  17 | br     | Breton                   | 36,338        | 4,759,407       | 31.4 MB          |
|  18 | bg     | Bulgarian                | 8,933,998     | 3,635,273,738   | 44.1 GB          |
|  19 | my     | Burmese                  | 430,276       | 82,433,836      | 3.0 GB           |
|  20 | ca     | Catalan                  | 6,953,898     | 2,240,460,836   | 15.3 GB          |
|  21 | ceb    | Cebuano                  | 16,174        | 6,263,404       | 41.1 MB          |
|  22 | ckb    | Central Kurdish          | 182,508       | 61,334,746      | 772.9 MB         |
|  23 | ce     | Chechen                  | 11,686        | 1,051,752       | 13.9 MB          |
|  24 | zh     | Chinese                  | 138,478,270   | 44,378,380,161  | 1.4 TB           |
|  25 | cv     | Chuvash                  | 16,652        | 3,039,925       | 42.3 MB          |
|  26 | kw     | Cornish                  | 8             | 80              | 432 Bytes        |
|  27 | hr     | Croatian                 | 31,808        | 3,542,961       | 26.5 MB          |
|  28 | cs     | Czech                    | 34,859,632    | 9,717,378,559   | 77.0 GB          |
|  29 | da     | Danish                   | 7,214,338     | 2,217,634,340   | 14.8 GB          |
|  30 | dv     | Divehi                   | 77,060        | 10,655,359      | 200.1 MB         |
|  31 | nl     | Dutch                    | 72,552,688    | 19,564,553,306  | 135.0 GB         |
|  32 | mhr    | Eastern Mari             | 9,502         | 1,615,215       | 22.9 MB          |
|  33 | arz    | Egyptian Arabic          | 3,958         | 385,511         | 3.7 MB           |
|  34 | en     | English                  | 1,235,510,986 | 523,869,288,690 | 3.4 TB           |
|  35 | eo     | Esperanto                | 226,924       | 67,774,923      | 474.8 MB         |
|  36 | et     | Estonian                 | 3,601,904     | 938,296,892     | 8.0 GB           |
|  37 | tl     | Filipino                 | 250,558       | 110,560,444     | 719.2 MB         |
|  38 | fi     | Finnish                  | 14,471,710    | 4,198,143,883   | 41.1 GB          |
|  39 | fr     | French                   | 158,334,998   | 62,127,088,294  | 430.5 GB         |
|  40 | gl     | Galician                 | 248,762       | 38,345,625      | 255.7 MB         |
|  41 | ka     | Georgian                 | 1,343,036     | 373,935,158     | 8.4 GB           |
|  42 | de     | German                   | 206,598,430   | 73,848,586,648  | 594.7 GB         |
|  43 | gom    | Goan Konkani             | 398           | 121,035         | 2.3 MB           |
|  44 | el     | Greek                    | 20,282,864    | 7,691,622,692   | 95.7 GB          |
|  45 | gn     | Guarani                  | 14            | 260             | 2.2 kB           |
|  46 | gu     | Gujarati                 | 425,552       | 417,001,705     | 5.6 GB           |
|  47 | ht     | Haitian Creole           | 2             | 20,671          | 93.1 kB          |
|  48 | he     | Hebrew                   | 3,997,888     | 1,697,158,891   | 18.0 GB          |
|  49 | hi     | Hindi                    | 5,514,454     | 2,475,605,444   | 32.6 GB          |
|  50 | hu     | Hungarian                | 21,349,372    | 16,013,364,289  | 150.1 GB         |
|  51 | is     | Icelandic                | 1,210,232     | 294,471,539     | 2.2 GB           |
|  52 | io     | Ido                      | 224           | 2,598           | 16.1 kB          |
|  53 | ilo    | Iloko                    | 144           | 4,411           | 28.0 kB          |
|  54 | id     | Indonesian               | 7,109,778     | 3,228,020,221   | 23.4 GB          |
|  55 | ia     | Interlingua              | 34            | 9,384           | 33.5 kB          |
|  56 | ie     | Interlingue              | 2             | 0               | 881 Bytes        |
|  57 | ga     | Irish                    | 29,894        | 9,054,923       | 63.2 MB          |
|  58 | it     | Italian                  | 89,021,606    | 36,327,274,203  | 259.4 GB         |
|  59 | ja     | Japanese                 | 94,236,404    | 4,401,059,165   | 181.2 GB         |
|  60 | jv     | Javanese                 | 172           | 3,286           | 25.7 kB          |
|  61 | xal    | Kalmyk                   | 2             | 27              | 315 Bytes        |
|  62 | kn     | Kannada                  | 448,500       | 124,924,350     | 2.6 GB           |
|  63 | krc    | Karachay-Balkar          | 496           | 8,385           | 122.4 kB         |
|  64 | kk     | Kazakh                   | 677,622       | 214,679,857     | 3.3 GB           |
|  65 | km     | Khmer                    | 450,660       | 59,880,231      | 3.2 GB           |
|  66 | kv     | Komi                     | 460           | 5,909           | 70.3 kB          |
|  67 | ko     | Korean                   | 15,147,698    | 3,435,866,935   | 38.1 GB          |
|  68 | ku     | Kurdish                  | 80,338        | 25,921,607      | 174.1 MB         |
|  69 | ky     | Kyrgyz                   | 144,288       | 32,062,783      | 489.3 MB         |
|  70 | lo     | Lao                      | 118,374       | 10,659,203      | 472.1 MB         |
|  71 | la     | Latin                    | 14,384        | 307,865         | 2.0 MB           |
|  72 | lv     | Latvian                  | 2,435,882     | 845,459,899     | 7.4 GB           |
|  73 | lez    | Lezghian                 | 676           | 60,634          | 856.6 kB         |
|  74 | li     | Limburgish               | 6             | 169             | 1.4 kB           |
|  75 | lt     | Lithuanian               | 5,182,028     | 1,674,362,574   | 14.5 GB          |
|  76 | jbo    | Lojban                   | 572           | 312,315         | 1.5 MB           |
|  77 | lmo    | Lombard                  | 112           | 3,269           | 21.0 kB          |
|  78 | nds    | Low German               | 5,248         | 1,612,175       | 10.7 MB          |
|  79 | dsb    | Lower Sorbian            | 8             | 84              | 664 Bytes        |
|  80 | lb     | Luxembourgish            | 18,090        | 2,514,838       | 18.4 MB          |
|  81 | mk     | Macedonian               | 1,063,298     | 389,344,425     | 4.7 GB           |
|  82 | mai    | Maithili                 | 46            | 467             | 6.8 kB           |
|  83 | mg     | Malagasy                 | 10,830        | 1,416,430       | 11.2 MB          |
|  84 | ms     | Malay                    | 11,500        | 238,477         | 2.6 MB           |
|  85 | ml     | Malayalam                | 800,936       | 236,597,838     | 5.8 GB           |
|  86 | mt     | Maltese                  | 5,180         | 149,886         | 1.3 MB           |
|  87 | mr     | Marathi                  | 729,578       | 252,706,331     | 4.5 GB           |
|  88 | mzn    | Mazanderani              | 384           | 16,115          | 169.2 kB         |
|  89 | min    | Minangkabau              | 2,436         | 305,589         | 3.8 MB           |
|  90 | xmf    | Mingrelian               | 7,318         | 283,316         | 6.1 MB           |
|  91 | mwl    | Mirandese                | 4             | 54              | 423 Bytes        |
|  92 | mn     | Mongolian                | 1,061,710     | 454,350,415     | 5.8 GB           |
|  93 | multi  | **Multilingual**         | 2,948,202     | 1,251,676,406   | 11.9 GB          |
|  94 | nah    | Nahuatl languages        | 38            | 279             | 2.4 kB           |
|  95 | ne     | Nepali                   | 1,152,156     | 278,901,036     | 4.9 GB           |
|  96 | new    | Newari                   | 1,996         | 229,703         | 4.0 MB           |
|  97 | no     | Norwegian                | 2,797,378     | 373,160,033     | 2.6 GB           |
|  98 | nn     | Norwegian Nynorsk        | 19,470        | 575,518         | 3.7 MB           |
|  99 | oc     | Occitan                  | 920           | 34,701          | 405.0 kB         |
| 100 | or     | Odia                     | 158,426       | 31,963,340      | 543.1 MB         |
| 101 | os     | Ossetic                  | 8,628         | 3,935,964       | 50.7 MB          |
| 102 | ps     | Pashto                   | 87,408        | 30,196,179      | 261.6 MB         |
| 103 | fa     | Persian                  | 23,813,882    | 9,609,206,698   | 93.2 GB          |
| 104 | pms    | Piedmontese              | 2,524         | 510,087         | 3.1 MB           |
| 105 | pl     | Polish                   | 57,184,826    | 18,073,705,588  | 147.1 GB         |
| 106 | pt     | Portuguese               | 36,062,800    | 15,172,557,311  | 105.0 GB         |
| 107 | pa     | Punjabi                  | 222,058       | 104,235,418     | 1.4 GB           |
| 108 | qu     | Quechua                  | 2             | 13              | 143 Bytes        |
| 109 | ro     | Romanian                 | 11,985,668    | 6,302,600,833   | 45.6 GB          |
| 110 | bxr    | Russia Buriat            | 72            | 698             | 8.2 kB           |
| 111 | ru     | Russian                  | 194,143,422   | 78,032,029,344  | 1.1 TB           |
| 112 | sah    | Sakha                    | 17,566        | 4,288,051       | 68.8 MB          |
| 113 | sa     | Sanskrit                 | 16,802        | 2,479,345       | 56.3 MB          |
| 114 | gd     | Scottish Gaelic          | 776           | 18,458          | 146.1 kB         |
| 115 | sr     | Serbian                  | 1,677,896     | 632,781,822     | 7.7 GB           |
| 116 | sh     | Serbian (Latin)          | 3,214         | 166,517         | 816.4 kB         |
| 117 | sd     | Sindhi                   | 48,566        | 14,667,207      | 131.6 MB         |
| 118 | si     | Sinhala                  | 301,066       | 172,755,385     | 2.6 GB           |
| 119 | sk     | Slovak                   | 8,931,784     | 2,704,716,280   | 21.5 GB          |
| 120 | sl     | Slovenian                | 1,112,560     | 192,816,743     | 1.4 GB           |
| 121 | so     | Somali                   | 6             | 51              | 503 Bytes        |
| 122 | azb    | South Azerbaijani        | 26,364        | 2,029,729       | 28.4 MB          |
| 123 | es     | Spanish                  | 153,574,556   | 63,388,237,965  | 429.9 GB         |
| 124 | su     | Sundanese                | 18            | 258             | 2.0 kB           |
| 125 | sw     | Swahili                  | 1,664         | 164,459         | 1.0 MB           |
| 126 | sv     | Swedish                  | 21,891,348    | 6,993,719,601   | 50.0 GB          |
| 127 | gsw    | Swiss German             | 342           | 34,328          | 232.7 kB         |
| 128 | tg     | Tajik                    | 144,932       | 76,987,285      | 1.0 GB           |
| 129 | ta     | Tamil                    | 1,638,238     | 738,824,392     | 15.8 GB          |
| 130 | tt     | Tatar                    | 262,654       | 59,253,765      | 833.8 MB         |
| 131 | te     | Telugu                   | 644,712       | 201,575,815     | 3.9 GB           |
| 132 | th     | Thai                     | 14,845,900    | 2,224,483,018   | 92.0 GB          |
| 133 | bo     | Tibetan                  | 62,352        | 6,062,558       | 531.6 MB         |
| 134 | tr     | Turkish                  | 26,654,330    | 8,290,890,087   | 73.7 GB          |
| 135 | tk     | Turkmen                  | 4,576         | 325,786         | 3.3 MB           |
| 136 | uk     | Ukrainian                | 10,059,992    | 3,183,842,018   | 44.7 GB          |
| 137 | x-eml  | Emiliano-Romagnol        | 4             | 329             | 1.8 kB           |
| 138 | hsb    | Upper Sorbian            | 402           | 15,827          | 123.2 kB         |
| 139 | ur     | Urdu                     | 887,004       | 434,023,273     | 3.8 GB           |
| 140 | ug     | Uyghur                   | 51,304        | 14,659,554      | 219.8 MB         |
| 141 | uz     | Uzbek                    | 15,806        | 1,665,960       | 15.3 MB          |
| 142 | vi     | Vietnamese               | 33,933,994    | 22,424,984,210  | 140.8 GB         |
| 143 | vo     | Volapük                  | 896           | 49,968          | 371.9 kB         |
| 144 | wa     | Walloon                  | 390           | 6,347           | 34.3 kB          |
| 145 | war    | Waray                    | 1,494         | 19,665          | 126.8 kB         |
| 146 | cy     | Welsh                    | 151,512       | 52,250,043      | 333.0 MB         |
| 147 | fy     | Western Frisian          | 45,458        | 9,885,788       | 70.4 MB          |
| 148 | mrj    | Western Mari             | 496           | 60,180          | 765.8 kB         |
| 149 | pnb    | Western Panjabi          | 12,904        | 11,844,695      | 105.8 MB         |
| 150 | wuu    | Wu Chinese               | 136           | 1,199           | 26.8 kB          |
| 151 | yi     | Yiddish                  | 47,438        | 14,287,370      | 171.7 MB         |
| 152 | yo     | Yoruba                   | 128           | 2,396           | 16.6 kB          |


## Dataset Creation

### Curation Rationale

OSCAR was constructed using [`Ungoliant`](https://github.com/oscar-corpus/ungoliant), a new pipeline derived from [goclassy](https://github.com/oscar-corpus/goclassy), itself being derived from [fastText's one](https://github.com/facebookresearch/fastText).

The pipeline works on documents rather than lines. 
`Ungoliant` is implemented in the [Rust programming language](https://rust-lang.org), and uses [rayon](https://github.com/rayon-rs/rayon) as its data parallelism strategy. 
Threading is done at shard, record and sentence level, making the whole generation process much more efficient.

Filtering will be explained in a future blog post at our [website](https://oscar-corpus.com)

### Source Data

#### Initial Data Collection and Normalization

[Common Crawl](https://commoncrawl.org/) is a non-profit foundation which produces and maintains an open repository of web crawled data that is both accessible and analysable. Common Crawl's complete web archive consists of petabytes of data collected over 8 years of web crawling. The repository contains raw web page HTML data (WARC files), metdata extracts (WAT files) and plain text extracts (WET files). The organisation's crawlers has always respected [nofollow](http://microformats.org/wiki/rel-nofollow) and [robots.txt](https://www.robotstxt.org/) policies.

Each monthly Common Crawl snapshot is in itself a massive multilingual corpus, where every single file contains data coming from multiple web pages written in a large variety of languages and covering all possible types of topics.

To construct OSCAR the WET files of Common Crawl were used. These contain the extracted plain texts from the websites mostly converted to UTF-8, as well as headers containing the metatada of each crawled document. Each WET file comes compressed in gzip format and is stored on Amazon Web Services. In the case of OSCAR 22.01, the **November/December 2021** snapshot was used. It is composed by 64 000 compressed text files containing documents and their headers.

#### Who are the source language producers?

The data comes from multiple web pages in a large variety of languages.

### Annotations

The dataset does not contain any additional annotations.

#### Annotation process

N/A

#### Who are the annotators?

N/A

### Personal and Sensitive Information

Being constructed from Common Crawl, Personal and sensitive information might be present. This **must** be considered before training deep learning models with OSCAR, specially in the case of text-generation models.

## Considerations for Using the Data

### Social Impact of Dataset

OSCAR is intended to bring more data to a wide variety of lanuages, the aim of the corpus is to make large amounts of data available to lower resource languages in order to facilitate the pre-training of state-of-the-art language modeling architectures.

### Discussion of Biases

OSCAR is not properly filtered yet and this can be reflected on the models trained with it. Care is advised specially concerning biases of the resulting models.

### Other Known Limitations

The [fastText linear classifier](https://fasttext.cc) is limed both in performance and the variety of languages it can recognize, so the quality of some OSCAR sub-corpora might be lower than expected, specially for the lowest-resource langiuages. Some audits have already been done by [third parties](https://arxiv.org/abs/2010.14571).

## Additional Information

### Dataset Curators

This release of OSCAR was made possible by [Julien Abadji](https://ujj.space), [Pedro Ortiz Suarez](https://portizs.eu/), [Rua Ismail](https://oscar-project.org/authors/rua/), [Sotaro Takeshita](https://sotaro.io/about), [Sebastian Nagel](https://www.polver.uni-konstanz.de/cnc/people/nagel/) and [Benoit Sagot](http://pauillac.inria.fr/~sagot/).

### Licensing Information

    These data are released under this licensing scheme
    We do not own any of the text from which these data has been extracted.
    We license the actual packaging, the metadata and the annotations of these data under the Creative Commons CC0 license ("no rights reserved") http://creativecommons.org/publicdomain/zero/1.0/
    To the extent possible under law, the OSCAR project, Inria, the Univertity of Mannheim and DFKI GmbH have waived all copyright and related or neighboring rights to OSCAR
    This work is published from: France and Germany.

    Should you consider that our data contains material that is owned by you and should therefore not be reproduced here, please:
    * Clearly identify yourself, with detailed contact data such as an address, telephone number or email address at which you can be contacted.
    * Clearly identify the copyrighted work claimed to be infringed.
    * Clearly identify the material that is claimed to be infringing and information reasonably sufficient to allow us to locate the material.

    We will comply to legitimate requests by removing the affected sources from the next release of the corpus.

### Citation Information

```
@ARTICLE{2022arXiv221210440J,
       author = {{Jansen}, Tim and {Tong}, Yangling and {Zevallos}, Victoria and {Ortiz Suarez}, Pedro},
        title = "{Perplexed by Quality: A Perplexity-based Method for Adult and Harmful Content Detection in Multilingual Heterogeneous Web Data}",
      journal = {arXiv e-prints},
     keywords = {Computer Science - Computation and Language},
         year = 2022,
        month = dec,
          eid = {arXiv:2212.10440},
        pages = {arXiv:2212.10440},
          doi = {10.48550/arXiv.2212.10440},
archivePrefix = {arXiv},
       eprint = {2212.10440},
 primaryClass = {cs.CL},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2022arXiv221210440J},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}

@inproceedings{abadji-etal-2022-towards,
    title = "Towards a Cleaner Document-Oriented Multilingual Crawled Corpus",
    author = "Abadji, Julien  and
      Ortiz Suarez, Pedro  and
      Romary, Laurent  and
      Sagot, Beno{\^\i}t",
    booktitle = "Proceedings of the Thirteenth Language Resources and Evaluation Conference",
    month = jun,
    year = "2022",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://aclanthology.org/2022.lrec-1.463",
    pages = "4344--4355",
    abstract = "The need for large corpora raw corpora has dramatically increased in recent years with the introduction of transfer learning and semi-supervised learning methods to Natural Language Processing. And while there have been some recent attempts to manually curate the amount of data necessary to train large language models, the main way to obtain this data is still through automatic web crawling. In this paper we take the existing multilingual web corpus OSCAR and its pipeline Ungoliant that extracts and classifies data from Common Crawl at the line level, and propose a set of improvements and automatic annotations in order to produce a new document-oriented version of OSCAR that could prove more suitable to pre-train large generative language models as well as hopefully other applications in Natural Language Processing and Digital Humanities.",
}

      
@inproceedings{AbadjiOrtizSuarezRomaryetal.2021,
  author    = {Julien Abadji and Pedro Javier Ortiz Su{\'a}rez and Laurent Romary and Beno{\^i}t Sagot},
  title     = {Ungoliant: An optimized pipeline for the generation of a very large-scale multilingual web corpus},
  series = {Proceedings of the Workshop on Challenges in the Management of Large Corpora (CMLC-9) 2021. Limerick, 12 July 2021 (Online-Event)},
  editor    = {Harald L{\"u}ngen and Marc Kupietz and Piotr Bański and Adrien Barbaresi and Simon Clematide and Ines Pisetta},
  publisher = {Leibniz-Institut f{\"u}r Deutsche Sprache},
  address   = {Mannheim},
  doi       = {10.14618/ids-pub-10468},
  url       = {https://nbn-resolving.org/urn:nbn:de:bsz:mh39-104688},
  pages     = {1 -- 9},
  year      = {2021},
  abstract  = {Since the introduction of large language models in Natural Language Processing, large raw corpora have played a crucial role in Computational Linguistics. However, most of these large raw corpora are either available only for English or not available to the general public due to copyright issues. Nevertheless, there are some examples of freely available multilingual corpora for training Deep Learning NLP models, such as the OSCAR and Paracrawl corpora. However, they have quality issues, especially for low-resource languages. Moreover, recreating or updating these corpora is very complex. In this work, we try to reproduce and improve the goclassy pipeline used to create the OSCAR corpus. We propose a new pipeline that is faster, modular, parameterizable, and well documented. We use it to create a corpus similar to OSCAR but larger and based on recent data. Also, unlike OSCAR, the metadata information is at the document level. We release our pipeline under an open source license and publish the corpus under a research-only license.},
  language  = {en}
}

@article{kreutzer-etal-2022-quality,
    title = "Quality at a Glance: An Audit of Web-Crawled Multilingual Datasets",
    author = {Kreutzer, Julia  and
      Caswell, Isaac  and
      Wang, Lisa  and
      Wahab, Ahsan  and
      van Esch, Daan  and
      Ulzii-Orshikh, Nasanbayar  and
      Tapo, Allahsera  and
      Subramani, Nishant  and
      Sokolov, Artem  and
      Sikasote, Claytone  and
      Setyawan, Monang  and
      Sarin, Supheakmungkol  and
      Samb, Sokhar  and
      Sagot, Beno{\^\i}t  and
      Rivera, Clara  and
      Rios, Annette  and
      Papadimitriou, Isabel  and
      Osei, Salomey  and
      Suarez, Pedro Ortiz  and
      Orife, Iroro  and
      Ogueji, Kelechi  and
      Rubungo, Andre Niyongabo  and
      Nguyen, Toan Q.  and
      M{\"u}ller, Mathias  and
      M{\"u}ller, Andr{\'e}  and
      Muhammad, Shamsuddeen Hassan  and
      Muhammad, Nanda  and
      Mnyakeni, Ayanda  and
      Mirzakhalov, Jamshidbek  and
      Matangira, Tapiwanashe  and
      Leong, Colin  and
      Lawson, Nze  and
      Kudugunta, Sneha  and
      Jernite, Yacine  and
      Jenny, Mathias  and
      Firat, Orhan  and
      Dossou, Bonaventure F. P.  and
      Dlamini, Sakhile  and
      de Silva, Nisansa  and
      {\c{C}}abuk Ball{\i}, Sakine  and
      Biderman, Stella  and
      Battisti, Alessia  and
      Baruwa, Ahmed  and
      Bapna, Ankur  and
      Baljekar, Pallavi  and
      Azime, Israel Abebe  and
      Awokoya, Ayodele  and
      Ataman, Duygu  and
      Ahia, Orevaoghene  and
      Ahia, Oghenefego  and
      Agrawal, Sweta  and
      Adeyemi, Mofetoluwa},
    journal = "Transactions of the Association for Computational Linguistics",
    volume = "10",
    year = "2022",
    address = "Cambridge, MA",
    publisher = "MIT Press",
    url = "https://aclanthology.org/2022.tacl-1.4",
    doi = "10.1162/tacl_a_00447",
    pages = "50--72",
    abstract = "With the success of large-scale pre-training and multilingual modeling in Natural Language Processing (NLP), recent years have seen a proliferation of large, Web-mined text datasets covering hundreds of languages. We manually audit the quality of 205 language-specific corpora released with five major public datasets (CCAligned, ParaCrawl, WikiMatrix, OSCAR, mC4). Lower-resource corpora have systematic issues: At least 15 corpora have no usable text, and a significant fraction contains less than 50{\%} sentences of acceptable quality. In addition, many are mislabeled or use nonstandard/ambiguous language codes. We demonstrate that these issues are easy to detect even for non-proficient speakers, and supplement the human audit with automatic analyses. Finally, we recommend techniques to evaluate and improve multilingual corpora and discuss potential risks that come with low-quality data releases.",
}

@inproceedings{ortiz-suarez-etal-2020-monolingual,
    title = "A Monolingual Approach to Contextualized Word Embeddings for Mid-Resource Languages",
    author = "Ortiz Su{'a}rez, Pedro Javier  and
      Romary, Laurent  and
      Sagot, Benoit",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.156",
    pages = "1703--1714",
    abstract = "We use the multilingual OSCAR corpus, extracted from Common Crawl via language classification, filtering and cleaning, to train monolingual contextualized word embeddings (ELMo) for five mid-resource languages. We then compare the performance of OSCAR-based and Wikipedia-based ELMo embeddings for these languages on the part-of-speech tagging and parsing tasks. We show that, despite the noise in the Common-Crawl-based OSCAR data, embeddings trained on OSCAR perform much better than monolingual embeddings trained on Wikipedia. They actually equal or improve the current state of the art in tagging and parsing for all five languages. In particular, they also improve over multilingual Wikipedia-based contextual embeddings (multilingual BERT), which almost always constitutes the previous state of the art, thereby showing that the benefit of a larger, more diverse corpus surpasses the cross-lingual benefit of multilingual embedding architectures.",
}

@inproceedings{OrtizSuarezSagotRomary2019,
  author    = {Pedro Javier {Ortiz Su{'a}rez} and Benoit Sagot and Laurent Romary},
  title     = {Asynchronous pipelines for processing huge corpora on medium to low resource infrastructures},
  series = {Proceedings of the Workshop on Challenges in the Management of Large Corpora (CMLC-7) 2019. Cardiff, 22nd July 2019},
  editor    = {Piotr Bański and Adrien Barbaresi and Hanno Biber and Evelyn Breiteneder and Simon Clematide and Marc Kupietz and Harald L{"u}ngen and Caroline Iliadi},
  publisher = {Leibniz-Institut f{"u}r Deutsche Sprache},
  address   = {Mannheim},
  doi       = {10.14618/ids-pub-9021},
  url       = {http://nbn-resolving.de/urn:nbn:de:bsz:mh39-90215},
  pages     = {9 -- 16},
  year      = {2019},
  abstract  = {Common Crawl is a considerably large, heterogeneous multilingual corpus comprised of crawled documents from the internet, surpassing 20TB of data and distributed as a set of more than 50 thousand plain text files where each contains many documents written in a wide variety of languages. Even though each document has a metadata block associated to it, this data lacks any information about the language in which each document is written, making it extremely difficult to use Common Crawl for monolingual applications. We propose a general, highly parallel, multithreaded pipeline to clean and classify Common Crawl by language; we specifically design it so that it runs efficiently on medium to low resource infrastructures where I/O speeds are the main constraint. We develop the pipeline so that it can be easily reapplied to any kind of heterogeneous corpus and so that it can be parameterised to a wide range of infrastructures. We also distribute a 6.3TB version of Common Crawl, filtered, classified by language, shuffled at line level in order to avoid copyright issues, and ready to be used for NLP applications.},
  language  = {en}
}

```
