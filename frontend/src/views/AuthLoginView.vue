<script setup lang="ts">
import '@/assets/auth.css'
import {ref, provide, onMounted, inject} from "vue";
import {useRouter} from "vue-router";

const router = useRouter();

// DO THIS
// const web_site = "mipt.site";
// const web_site = "localhost";
// const web_site = "127.0.0.1";
const web_site = inject('web_site');

const username = ref<String>("");
const password = ref<String>("");

let error_message = ref<String>("");

async function sendForm(){
  try {
    const response = await fetch("https://" + web_site + ":8088" + "/token/",{
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        'username': username.value,
        'password': password.value
      })
    });

    const data = await response.json();
    console.log('Ответ от сервера:', data);

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);
      error_message.value = data?.non_field_errors[0] || "Ошибка авторизации";
    }


    if("token" in data){
      localStorage.setItem("auth-token", data.token);
      error_message.value = "Успешная авторизация!";
      setTimeout(()=>{
          router.push("/profile/").then(()=>{
            router.go(0); // force reload
          });
      }, 1000);
      return;
    }

  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}

</script>

<template>
	<div class="center-div-login">
		<!-- <h2>Авторизация</h2>-->
  		<form @submit.prevent="sendForm">
			<h2>Авторизация</h2>
			
			<head>
    				<script src="https://yastatic.net/s3/passport-sdk/autofill/v1/sdk-suggest-with-polyfills-latest.js"></script>
			</head>
    			
			<h4>Введите логин</h4>
    			<input class="center-button auth-input" type="text" name="username" v-model="username">
    
			<h4>Введите пароль</h4>
    			<input class="center-button auth-input" type="password" name="password" v-model="password">
    
			<span style="margin: 8px">{{error_message}}</span>
    			<input type="submit" value="Авторизоваться" class="button-auth center-button">
			<p style="text-align: center; color: gray;">или войти с помощью</p>
			
			<a href="https://oauth.yandex.ru/authorize?response_type=token&client_id=fc1c3b1661c643a09f6c3622818b3275" style="text-decoration: none;">
				<div style="background: black; display: flex;" class="button-auth center-button-auth">
				  <div class="auth-text-class" style="">
				    <img style="width: 24px; padding-right: 10px;" src="https://upload.wikimedia.org/wikipedia/commons/5/58/Yandex_icon.svg"  alt="Логотип Yandex">
				  </div>
			          <div style="">
				    Яндекс ID
				  </div>
				</div>
			</a>
  		</form>
	</div>
</template>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.center-div-login{
	padding-top: 15vh;
}

/*Стили для мобильных устройств (экраны меньше 768px) */
@media (max-width: 768px) {
    .center-button {
        width: 80%; /*Растягиваем на всю ширину экрана */
    }
    .center-button-auth {
        width: 80vw; /*Растягиваем на всю ширину экрана */
    }
    .auth-text-class {
	padding-left: 30%;
    }
}

/*Стили для планшетов и компьютеров (экраны от 768px) */
@media (min-width: 768px) {
    .center-button {
        width: 30%; /*Ограничиваем ширину до 80% */
    }
    .center-button-auth {
        width: 30vw; /*Растягиваем на всю ширину экрана */
    }
    .auth-text-class {
        padding-left: 40%;
    }

}


/*Базовые стили */
.auth-input {
  /* width: 100%; */
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box; /*Чтобы паддинг и бордер не увеличивали ширину */
  font-size: 16px;
  margin-bottom: 10px; /*Отступ снизу */
}

/*Стили при фокусе */
.auth-input:focus {
  outline: none; /*Убираем стандартный контур */
  border-color: #007bff; /*Синий цвет границы при фокусе */
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.2); /*Небольшой эффект тени */
}

/*Стили при ошибке */
.auth-input.error {
  border-color: #dc3545; /*Красный цвет границы при ошибке */
  box-shadow: 0 0 5px rgba(220, 53, 69, 0.2); /*Красная тень при ошибке */
}

</style>
