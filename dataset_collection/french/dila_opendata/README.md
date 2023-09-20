# DILA OpenData

French Government OpenData from the [DILA](https://echanges.dila.gouv.fr/OPENDATA/"). This includes LegiFrance data, as 
well as a variety of administrative and legal textual data.

### Downloading 

```bash
 wget -r -np -R "index.html*" https://echanges.dila.gouv.fr/OPENDATA/ -P dataset_collection/french/dila_opendata/data 
```

To download select subfolders only:

```bash
```bash
 wget -r -np -R "index.html*" https://echanges.dila.gouv.fr/OPENDATA/LEGI/ -P dataset_collection/french/dila_opendata/data 
 wget -r -np -R "index.html*" https://echanges.dila.gouv.fr/OPENDATA/Questions-Reponses/ -P dataset_collection/french/dila_opendata/data 
 wget -r -np -R "index.html*" https://echanges.dila.gouv.fr/OPENDATA/JADE/ -P dataset_collection/french/dila_opendata/data 
 wget -r -np -R "index.html*" https://echanges.dila.gouv.fr/OPENDATA/INCA/ -P dataset_collection/french/dila_opendata/data 
 wget -r -np -R "index.html*" https://echanges.dila.gouv.fr/OPENDATA/CNIL/ -P dataset_collection/french/dila_opendata/data 
 wget -r -np -R "index.html*" https://echanges.dila.gouv.fr/OPENDATA/CONSTIT/ -P dataset_collection/french/dila_opendata/data 
 wget -r -np -R "index.html*" https://echanges.dila.gouv.fr/OPENDATA/DEBATS/ -P dataset_collection/french/dila_opendata/data 
 wget -r -np -R "index.html*" https://echanges.dila.gouv.fr/OPENDATA/KALI/ -P dataset_collection/french/dila_opendata/data 
 wget -r -np -R "index.html*" https://echanges.dila.gouv.fr/OPENDATA/DOLE/ -P dataset_collection/french/dila_opendata/data 

```

Data are under open-use license described in the [license](https://www.etalab.gouv.fr/wp-content/uploads/2017/04/ETALAB-Licence-Ouverte-v2.0.pdf) file.

Large quantities of data are available, in particular:

In /ACCO, are the Accords d'Entreprise.
in /AMF, are the Autorité des Marchés Financiers data.

### Preprocessing

To parse XML document and retrieve the text body, run script with:
```bash
python scrapping.py --base_path data/echanges.dila.gouv.fr/OPENDATA/LEGI --save_dir data/ --prefix LEGI --hub_id manu/dila_legifrance
python scrapping.py --base_path data/echanges.dila.gouv.fr/OPENDATA/KALI --save_dir data/ --prefix KALI --hub_id manu/dila_kali
python scrapping.py --base_path data/echanges.dila.gouv.fr/OPENDATA/Questions-Reponses --save_dir data/ --prefix QR --hub_id manu/dila_questions_reponses
python scrapping.py --base_path data/echanges.dila.gouv.fr/OPENDATA/CNIL --save_dir data/ --prefix CNIL --hub_id manu/dila_cnil
```

## SLURM

```bash
sbatch --job-name=cpu --nodes=1 --time=4:00:00 -p cpu_med --cpus-per-task 16 --error=log.err --output=log.out --wrap="`python scrapping.py --base_path data/echanges.dila.gouv.fr/OPENDATA/LEGI --save_dir data/ --prefix LEGI --hub_id manu/legifrance"
```


### Extra datasets - already cleaned

On the hub: `StanBienaives/french-open-fiscal-texts`