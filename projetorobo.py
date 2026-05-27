import os

# =========================
# REMOVE AVISOS
# =========================

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# =========================
# IMPORTS
# =========================

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import cv2
import requests

from sklearn.utils.class_weight import compute_class_weight

# =========================
# WIFI DO ROBÔ (ESP32)
# =========================

ESP32_IP = "http://192.168.4.1"

# =========================
# DATASET
# =========================

dataset = "dataset"

print("Classes encontradas:")
print(os.listdir(dataset))

# =========================
# TREINO
# =========================

train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    dataset,
    validation_split=0.2,
    subset='training',
    seed=123,
    image_size=(224, 224),
    batch_size=8
)

validation_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    dataset,
    validation_split=0.2,
    subset='validation',
    seed=123,
    image_size=(224, 224),
    batch_size=8
)

class_names = train_dataset.class_names

print("\nClasses:")
print(class_names)

# =========================
# PESOS DAS CLASSES
# =========================

labels = np.concatenate([y for x, y in train_dataset], axis=0)

class_weight = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(labels),
    y=labels
)

class_weight = dict(enumerate(class_weight))

print("\nPesos das classes:")
print(class_weight)

# =========================
# DATA AUGMENTATION
# =========================

data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.2),
    tf.keras.layers.RandomZoom(0.2),
])

# =========================
# MODELO BASE
# =========================

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)

base_model.trainable = True

# congela primeiras camadas
for layer in base_model.layers[:100]:
    layer.trainable = False

# =========================
# MODELO FINAL
# =========================

model = tf.keras.Sequential([

    data_augmentation,

    tf.keras.layers.Rescaling(1./127.5, offset=-1),

    base_model,

    tf.keras.layers.GlobalAveragePooling2D(),

    tf.keras.layers.Dropout(0.5),

    tf.keras.layers.Dense(2, activation='softmax')
])

# =========================
# COMPILAR
# =========================

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-4),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# =========================
# EARLY STOPPING
# =========================

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True
)

# =========================
# TREINAMENTO
# =========================

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=50,
    class_weight=class_weight,
    callbacks=[early_stopping]
)

# =========================
# SALVAR MODELO
# =========================

model.save("modelo_planta.keras")

print("\nModelo salvo com sucesso!")

# =========================
# GRÁFICOS
# =========================

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

plt.figure(figsize=(12,5))

# accuracy
plt.subplot(1,2,1)

plt.plot(acc, label='Treino')
plt.plot(val_acc, label='Validação')

plt.title('Accuracy')

plt.legend()

# loss
plt.subplot(1,2,2)

plt.plot(loss, label='Treino')
plt.plot(val_loss, label='Validação')

plt.title('Loss')

plt.legend()

plt.show()

# =========================
# CÂMERA AO VIVO + ROBÔ
# =========================

print("\nAbrindo câmera... pressione Q para sair")

cap = cv2.VideoCapture(0)

ultimo_estado = None

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # preparar imagem
    img = cv2.resize(frame, (224, 224))

    img = img / 255.0

    img = np.expand_dims(img, axis=0)

    # previsão
    prediction = model.predict(img, verbose=0)

    classe = np.argmax(prediction[0])

    confianca = prediction[0][classe] * 100

    label = class_names[classe]

    texto = f"{label} ({confianca:.2f}%)"

    # =========================
    # ENVIO PARA ESP32
    # =========================

    try:

        if classe != ultimo_estado:

            if classe == 0:
                requests.get(f"{ESP32_IP}/ok")

            elif classe == 1:
                requests.get(f"{ESP32_IP}/doente")

            ultimo_estado = classe

    except:
        print("Erro ao conectar com ESP32")

    # mostrar resultado na tela
    cv2.putText(
        frame,
        texto,
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Robo IA - Plantas", frame)

    # sair com Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()

# =========================
# TESTE FINAL COM IMAGEM
# =========================

image_path = "dataset/Potato___healthy/plantaboa_94.JPG"

# carregar imagem
img = tf.keras.preprocessing.image.load_img(
    image_path,
    target_size=(224,224)
)

# =========================
# MOSTRAR IMAGEM
# =========================

plt.figure(figsize=(5,5))

plt.imshow(img)

plt.title("Imagem Testada")

plt.axis("off")

plt.show()

# =========================
# PREPARAR IMAGEM
# =========================

img_array = tf.keras.preprocessing.image.img_to_array(img)

# normalizar
img_array = img_array / 255.0

# adicionar dimensão
img_array = np.expand_dims(img_array, 0)

# =========================
# PREVISÃO
# =========================

prediction = model.predict(img_array)

classe = np.argmax(prediction[0])

# =========================
# RESULTADO FINAL
# =========================

print("\n=========================")
print("IMAGEM ANALISADA:")
print(os.path.basename(image_path))
print("=========================")

print("\nResultado do teste:")

for i, nome in enumerate(class_names):

    print(f"{nome}: {prediction[0][i] * 100:.2f}%")

print("\nClasse prevista:")
print(class_names[classe])
