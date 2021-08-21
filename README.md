# MathB_Dataset
Dataset containing mathematical expressions.</br>
The dataset files are present in <b>MathyB Dataset files</b> folder. If you want to access the expressions captured by ME detector tool for all the projects, then those files are present in this <a href="https://drive.google.com/drive/folders/15BeaiKLpynYsgZNrJ_X0hnvFiA2H9NN-?usp=sharing" target="_blank">drive link</a>. </br>
Overleaf link for presentation is <a href="https://www.overleaf.com/3384518454xxspgssgvpqz">here</a>. </br>
Overleaf link for paper is <a href="https://www.overleaf.com/5588149215pwtgvwyktrtd">here</a>.
## Rules:
### Rule 1:
<ui>

 <li> Math functions like <b>Math.exp</b>, <b>Math.log</b>, <b>Math.tan</b>, <b>Math.sin</b>, <b>Math.cos</b>,<b>Math.tan</b>, <b>Math.sinh</b>, <b>Math.cosh</b>, <b>Math.atan</b>, <b>Math.acot</b>,<b> Math.abs</b> present in the bug report </li>
 </ui>

### Rule 2:
<ui>
    <li> Numbers containing scientific notation like 1.0e2,1E-1 </li>
</ui>

### Rule 3:
<ui>
  <li> Constants like Nan, Math.PI, inf, etc. </li>
</ui>

### Rule 4:
<ui>
<li> Numerical sets or sequences contained within closed brackets i.e. {},(),[] and having atleast 2 elements e.g.{-1.1,2.05},(1,2) or [1,2,3]. </li>
</ui>

### Rule 5:
<ui>
<li> complex numbers : Numbers of the form x+iy,x+yi where x and y can be any real number. </li>
</ui>

### Rule 6:
<ui>
<li> Sets or sequences containing constants mentioned in Rule ID 4 within closed brackets i.e. {},(),[] and having at least 2 elements. </li>
 </ui>


### Rule 7:
<ui>
  <li>Each of the operators +,-,*,=,%,/,<,>,! and * occuring twice,consecutively, and followed by a number</li>
 </ui>

### Rule 8:
<ui>
<li> Each of the operators +,-,*,=,\%,/,<,> and * occuring atleast once and must be followed by atleast one digit </li>
 </ui>
 
### Rule 9:
<ui>
<li> Atleast one digit followed by 0 or more digits and followed by one or two of the operators +,-,*,=,%,/,<,>,! and * which must be followed by atleast one character (a-zA-Z) and followed by 0 or more characters </li>
 </ui>
 
### Rule 10:
<ui>
 <li> Atleast one character (a-zA-Z) followed by zero or more characters and followed by atleast one of the operators +,-,*,=,\%,/,<,>,!,* which must be followed by atleast one digit and followed by any number of digits </li>
 </ui>
 
### Rule 11:
<ui>
<li> Contiguous operators and numbers : there must be atleast 2 digits and 2 operators from +,-,*,=,%,/,<,>,! and *. </li>
 </ui>
 
### Rule 12:
<ui>

<li> Dimensions or shapes of matrices and arrays separated by * or x like 250x250 or 250 * 250 </li>
 </ui>

## NNGen
 We provide ME removed data for NNGen in this repo. Kindly refer to this Gihub repo https://github.com/Tbabm/nngen for commands on running the NNGen project.
