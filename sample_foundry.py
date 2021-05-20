from foundry import Foundry
import pandas as pd

# read in relevant data
data = pd.read_csv('iris.csv', header=1)
# set model options
options_sklearn = {"title": "Iris SVM (test pub repeat)",
            "short_name": "AS_iris_svm_test_publish",
            "authors": ["Scourtas, A"],
            "servable": {
                "type": "sklearn",
                "filepath": "model.pkl",
                "classes": data['species'].unique(),
                "n_input_columns": len(data.columns) - 1
            }
           }

options_keras = {
            "title": "test keras publication",
            "short_name": "AS_test_model_publish_keras",
            "authors": ["Scourtas, A"],
            "servable": {
                "type": "keras",
                "model_path": "model.hdf5",
                "output_names": list(map(str, range(10)))

            }
}

# publish model
f = Foundry()
# res = f.publish_model(options_sklearn)
# res = f.publish_model(options_keras)
print("iosjdoadijas")
# yay it's done!!
# res = f.run('aristana_uchicago/AS_iris_svm_test_publish', [[6.7,3.1,4.4,1.4], [4.8,3.0,1.4,0.1], [7.2,3.6,6.1,2.5]])
# res = f.run('zhuozhao_uchicago/Noop', [1, 2, 3, 2, 2, 3])
# print(res)