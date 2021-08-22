# Mathematical Expressions in Software Engineering Artifacts
### MathyB dataset
<ul>
<li>To run MEDSEA: A Mathematical Expression Detector Tool for Software Engineering Artifacts on projects mentioned in the paper, download the folder <b>Bug_data</b> from https://zenodo.org/record/5229831#.YSFg644zZPY. </li>
<li>Then run this command:</li>
</ul>
```python
$ python MEFinder.py -input_path [path of the input project file which should be a .xlsx file] -output_path [path of the output file which should be a .csv file] - preprocessing [True or False]
```
The default settings are:
```python
$ python MEFinder.py -input_path Bug_data_linux.xlsx -output_path LINUX.csv - preprocessing True
```
<ul>
 <li> Set <b>input_path</b> to the .xlsx file in <b>Bug_data</b> folder. Also, set preprocessing to False if you do not want to remove URLs and collection of black listed words. 
<li> Each column in <b>ME_RULES.csv</b> corresponds to the collection of operators or mathemtical fucntions corresponding to that rule. Columns corresponding to rules 1 to 12 are named so in the file. The last column is the collection of black listed words. If you want to add/remove regex based rules then change them accordingly in the ME_RULES.csv file and in MEFinder.py. Make sure ME_remove_words is the last column in the file. </li>
<li> You can test our tool on custom input at the web version of our tool available at the <a href="https://share.streamlit.io/mathyb/mathyb_dataset/main/website/MedSea.py">project site</a></li></ul>

### NNGen
To evaluate NNGen with the modified data (Mathematical Expression removed code differences), download the dataset <b>NNGen_modified_data</b> from https://zenodo.org/record/5229831#.YSFg644zZPY and follow the instructions at https://github.com/Tbabm/nngen to execute the NNGen task.
