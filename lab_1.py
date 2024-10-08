# -*- coding: utf-8 -*-
"""Lab-1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10gX8unTPqkg-i8cpb0pxgzkrdIuFb9HK
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

data = pd.read_excel('2024-09-23 Sotsiologicheskii opros.xlsx')

data = data.drop(columns=['Как часто вы берете инициативу в свои руки? / Баллы',
                          'Как часто вы пропускаете завтраки? / Баллы',
                          'Какая культура ближе / Баллы',
                          'Выпиваете алкоголь / Баллы',
                          'Формат работы / Баллы',
                          'Любимое время года? / Баллы',
                          'Что пьют родители / Баллы',
                          'Какие напитки любите / Баллы',
                          'Набрано баллов',
                          'Всего баллов',
                          'Результат теста'])

X = data.drop('Что вы предпочитаете?', axis=1)
y = data['Что вы предпочитаете?']

categorical_columns = X.select_dtypes(include=['object']).columns

encoder = OneHotEncoder(sparse_output=False)
X_encoded = pd.DataFrame(encoder.fit_transform(X[categorical_columns]))

X_encoded.columns = encoder.get_feature_names_out(categorical_columns)
X_final = pd.concat([X.drop(columns=categorical_columns), X_encoded], axis=1)

scaler = StandardScaler()
X_final_normalized = pd.DataFrame(scaler.fit_transform(X_final), columns=X_final.columns)


X_train, X_test, y_train, y_test = train_test_split(X_final_normalized, y, test_size=0.2, random_state=1)


knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)


results = pd.DataFrame({'Реальный ответ': y_test, 'Предсказанный ответ': y_pred})
print(results)

accuracy = accuracy_score(y_test, y_pred)
print(f"Точность модели: {accuracy * 100:.2f}%")

num_string = 38

new_record = X_final_normalized.iloc[num_string:num_string+1]

prediction = knn.predict(new_record)

probabilities = knn.predict_proba(new_record)

print("Предсказание:", *prediction)
print("Вероятности:", *probabilities)