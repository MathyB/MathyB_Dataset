# Mathematical Expressions in Software Engineering Artifacts
### MathyB dataset
<ul>
<li>To run MEDSEA: A Mathematical Expression Detector Tool for Software Engineering Artifacts, download the dataset from https://zenodo.org/record/3965149#.YSDic44zZPY. </li>
<li>Change the <b>INPUT_PATH</b> in MEFinder.py to the location of the project in your local system and <b>OUTPUT_PATH</b> to the location in your local system where you want to save the output. </li>
 <li><b>remove_status</b> in MEFinder.py manages whether MEDSEA should ignore URLs and collection of black listed words while scanning through the bug reports. Default value of <b>remove_status</b> is True. You can change its value between True and False according to your wish.</li>
Then run this command:
```python
$ python MEFinder.py
```

The web version of our tool is available at the <a href="https://share.streamlit.io/mathyb/mathyb_dataset/main/MEFinder.py">project site</a>
### NNGen
 We provide ME removed data for NNGen in this repo. Kindly refer to this Gihub repo https://github.com/Tbabm/nngen for commands on running the NNGen project.
