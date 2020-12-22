# CodeAndData
## AnalyzeAPK
Analyze apk files to get mappings between features and APIs.
## Usage
- The steps to use the program are as follows：

  Firstly, using ***AnalyzeAPKFile.py*** to parse the APK file to get the correspondence between methods in the APK file and the APIs called by the methods.The APK file as the input in this step and the corresponding relationships of the methods implemented in the APK file and the APIs called by the methods as the output.
  
  Secondly, using ***GetMappings.py*** to establish the correspondence between features and method names in the feature framework, and further analyze the mappings of the features and the API used by the App to implement the features. In this step, we use the result obtained in the first step as input and use App descriptions as training data to train word2vec for calculating the semantic similarity between features and method names. By analyzing the results, we can get the mapping between features, methods and APIs as the output. 
## Example
Several APK files and results gained after processing them with the code in AnalyzeAPK.
