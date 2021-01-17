Title: Exploring 4 Ways to Predict the Probability of a Bug in a Commit
Date: 2021-01-17

Every commit has a risk, and that risk varies. Teams go through a process to reduce that risk, but whether it's a single line code change or vast refactor, it's often the same process. Quantifying the risk based on previous similar commits can help us decide whether it's worth spending a bit more time than usual. Experienced teams have good intuition when deciding whether they've done enough, but cognitive biases can lead us astray. Stats can help with that. 

## The Data

For this example I've run some analysis on [SonarQube](https://github.com/SonarSource/sonarqube). Most developers will have come across this popular static analysis tool for finding bugs and security issues in code. It's an interesting repo because it appears to have a low defect rate (2 issues per 1000 lines of code added) and small variance between developers. It looks like they eat there own dog food and deliver some very high quality code. 

![SonarQube Author Distribution]({static}/images/sonarqube_analysis.png)

I extracted more than 20,0000 commits spanning the last 10 years, shuffled them, and split them 60/40 into a training and test set. For each commit I've extracted the author, a count of the lines of code added and tokenised the code for use in the machine learning methods later in the article. 


### A baseline: Linear Regression on Lines of Code Added

Bugs resides in code, so it follows that more code will increase the probability of more bugs. We can model this with linear regression using Numpy's polyfit function. This function derives the coefficients for least squares polynomial fit. We can specify the number of degrees to use and the coefficients can be passed to the poly1d function that returns a function we can use.

```python
#linear regression
coeffs = np.polyfit(xtrain, ytrain, 1)
f1 = np.poly1d(coeffs)
print(f1)
0.001064 x + 0.2746
```

We can then use these functions to predict the probability of a bug in our test dataset and pass the results to a validator. For all these experiments I've used the BinaryAccuracy Validator in Keras for consistency

```python
validator = tf.keras.metrics.BinaryAccuracy()
validator.update_state(ytest, f1(xtest))
print('f1:',validator.result().numpy())
f1: 0.69960284
```

These methods give us 70-72% Accuracy. It's a good place to start

| Degree Polynomial | Function | Accuracy |
|:----------------- |:--------- |:----------- |
| 1st               | 0.001064x + 0.2746 |70%         |
| 2nd               | -2.424e-06x² + 0.002654x + 0.2112|71.6%       |
| 3rd               | 5.956e-09x³ - 9.318e-06x² + 0.004362x + 0.1732|72.2%       |


Here's the curves. It's interesting to see that on the 3rd Degree Polynomial there is a relatively flat section between 200-700 Lines of Code Added (LOCA) and then a rapid rise in risk. This might suggest that after 700 LOCA the commit becomes to large for us to safely comprehend and we miss problems.

![PR Review Image]({static}/images/charts/regression.png)

### Developers are different: A Curve for each Committer
From the histogram at the beginning of this post we can see that although the variance between developers is relatively low at Sonar it's still significant, and if we factor this into a model we should see a more accurate result. The code below creates a function for every developer with over 100 commits and defaults to the general case for those with less. 

```python
authors = {}
for author, group in train_df.groupby('author'):
    if len(group) > 100:
        coeffs = np.polyfit(group.locadd, group.labels, 3)
        function = np.poly1d(coeffs)
        authors[author] = function

def auth_specific(author, locadd):
    author_func = authors.get(author)
    if author_func:
        return author_func(locadd)
    else:
        return f3(locadd)

test_predicted = []
for index, commit in test_df.iterrows():
    test_predicted.append(auth_specific(commit['author'], commit['locadd']))


validator = tf.keras.metrics.BinaryAccuracy()
validator.update_state(test_df['labels'], test_predicted)
print('auth_specific:',validator.result().numpy())
auth_specific: 0.7364434
```
Sure enough this approach does improve the overall accuracy of our predictions to **73.6%**. 
| Degree Polynomial | Function | Accuracy |
|:----------------- |:--------- |:----------- |
| 3rd               | Bespoke per committer |73.6%         |

![PR Review Image]({static}/images/charts/author_regression.png)

### A bit of AI: A basic Neural Network
So far we've only considered the size of the commit and the author but another factor we should consider is the type of code that was changed. Finding useful representations in unstructured code data is a job for machine learning, in this case we'll Neural Networks and Natural Language Processing techniques. 

First up is a basic NLP Neural Network using word embeddings and a single dense layer. The training sequences passed contain sequences for a string that starts with the author and then includes all the code in the commit. 

```python
from keras.models import Sequential
from keras.layers import Flatten, Dense, Embedding, Dropout


model = Sequential()
model.add(Embedding(len(data_sonar.tokenizer.word_index), 16, input_length=10000))
model.add(Flatten())
model.add(Dense(1, activation='sigmoid'))
model.summary()
model.compile(
    optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.00001), 
    loss='binary_crossentropy', 
    metrics=[tf.keras.metrics.BinaryAccuracy()])
model.fit(data_sonar.train_sequences, data_sonar.train_labels,
    epochs=30,
    batch_size=8,
    validation_split=0.33)
model.evaluate(data_sonar.test_sequences, data_sonar.test_labels)
```

This gives us an accuracy of **72.8%** very close to our authors curves method. Whilst this version doesn't beat the previous method it's a great starting point for machine learning. Lets try something a bit more sophisticated. 

### A Bit More AI: A Convnet

Finally lets try a Convnet. Convnets or Convolutional Neural Networks are commonly used for image recognition but can but can perform well on text processing. They work in a similar way to the neurons in our visual cortex by finding abstractions and passing these simpler representations to the next layer. It's possible that they may discover patterns in code that can increase the probability of a bug. Lets give it a try...

```python
model = Sequential()
model.add(Embedding(len(data_sonar.tokenizer.word_index), 128, input_length=10000))
model.add(layers.Conv1D(32, 7, activation='relu'))
model.add(layers.MaxPool1D(5))
model.add(layers.Conv1D(32, 7, activation='relu'))
model.add(layers.GlobalMaxPool1D())
model.add(Dense(1, activation='sigmoid'))
model.summary()
model.compile(
    optimizer=tf.keras.optimizers.RMSprop(learning_rate=1e-4), 
    loss='binary_crossentropy', 
    metrics=[tf.keras.metrics.BinaryAccuracy()])
model.fit(data_sonar.train_sequences, data_sonar.train_labels,
    epochs=25,
    batch_size=8,
    validation_split=0.33)
model.evaluate(data_sonar.test_sequences, data_sonar.test_labels)
```

The result of this simple implementation on the SonarQube repo is very slightly improved with 73.6% Accuracy. 

### Conclusion 

| Repo      | Linear Regression | 2D Polynomial | 3D Polynomial | Author Bespoke Polynomial | Simple NN | Convnet
|:----      |:----------------- |:------------- |:------------- | :-------------------------| :---------| :-----
| SonarQube | 69% | 71% | 72% | 70% | 73% | 73%
| AspNet Core | 77%? | 77%? | 78% | 80% | 80%
| Angular | 67% | 70% | 72% | 70% | 73%

Bugs are hard to predict, but when we raise awareness of the risk before the damage is done, we can save a lot of pain later and increase development flow. Whilst these simple machine learning approaches don't offer any advantage of a statistical approach, they do seem to have the potential to recognise patterns of risky code which should significantly raise accuracy of predictions. If you're interested in exploring this further on your repos please get in touch or try [ReviewML](https://www.solittlecode.com/reviewml).

