<script setup lang="ts">

import Header from "@/components/TheHeader.vue";
import {ref, type Ref, onMounted, reactive, type Reactive, inject, provide} from 'vue';
// import type {sharedVariable} from "@/classes/Interfaces";

interface BBNumber {
  username: string,
  number_bb: number
}
interface UserName {
  first_name: string,
  last_name: string,
  third_name: string
}
interface Preference {
  name: string,
  description: string
}
interface InstituteGroup {
  name: string,
  description: string
}


// DO THIS
// const web_site = "mipt.site";
// const web_site = "localhost";
// const web_site = "127.0.0.1";
const web_site = inject('web_site');

let username = ref<string|null>(null);
let number_bb = ref<string|null>(null);

let form_first_name = ref<string|null>(null);
let form_last_name = ref<string|null>(null);
let form_third_name = ref<string|null>(null);
let selected_institute_group = ref<string|null>(null);
let search_institute_group = ref<string|null>(null);

let token = ref<string|null>(null);

const user_name: Reactive<UserName> = reactive({
  first_name: "", last_name: "", third_name: ""
});
let institute_group: Ref<string|null> = ref(null);
let book_rating: Ref<number> = ref(1);
let preferences: Ref<Preference[]> = ref([]);
let user_preferences: Ref<Preference[]> = ref([]);
let institute_groups: Ref<InstituteGroup[]> = ref([]);


type KeyValuePair = [string, string];

let preferencesIcons: Record<string, string> = {
  "Тишина": "@/assets/cloud.svg",
  "Свежий воздух": "@/assets/cloud.svg",
  "Тихая музыка": "@/assets/cloud.svg"
};

onMounted(()=>{
  // начинаем авторизацию пользователя обрабатывая все возможные случаи комбинации токенов
  if (token.value == null){ //  рассматриваем начальный случай когда пустой токен неопределён
	if (localStorage.getItem("auth-token") == null) { //  рассматриваем случай когда хронилище токена пустое
	    sendAuthGet().then(() => { //  делаем запрос к яндексу для получения данных пользователя
		token.value = localStorage.getItem("auth-token");
		username.value = localStorage.getItem("username");
	    }).then(() => { //  загружаем нужные для отображения данные с микросервисов
	        console.log("===== 02");
        	if(token.value == null) return;
        	
		console.log("===== 03");
		loadInfo();
        	loadPreferences();
        	loadBBNumber();
	    }).then(() => {
	        if (token.value == null) {
		    console.log("go to auth page");
		} 
		else {
		    router.go(0);}
	    });
	}
	else { //  обрабатываем случай когда токен созранён - в таком случае подгружаем данные из БД
	    logAuth().then(() => { //  делаем запрос к яндексу для получения данных пользователя
		token.value = localStorage.getItem("auth-token");
                username.value = localStorage.getItem("username");
	    }).then(() => { //  загружаем нужные для отображения данные с микросервисоv
                if(token.value == null) return;

                loadInfo();
                loadPreferences();
                loadBBNumber();
	    });
	}
  }
  else {
  	console.log("===== 1");
  	if(token.value == null) return;
  	console.log("===== 2");
  	loadInfo();
  	console.log("===== 3");
  	loadPreferences();
  	console.log("===== 4");
  	loadBBNumber();
  }
  loadInstituteGroup();
});

import { useRouter } from 'vue-router';

const router = useRouter();

async function logout() {
  try {
    if (1 == 1) {
      // Удалите токен из LocalStorage
      localStorage.removeItem('auth-token');
      localStorage.removeItem('username');
      // Перенаправьте пользователя на страницу входа
      // this.$router.push('auth');
      // this.router.push({ path: 'auth' });
      // router.push('auth');
      router.go(0);
    } else {
      // Обработайте ошибку
    }
  } catch (error) {
    // Обработайте ошибку
  }
}

async function loadInfo(){
  try {
    const response = await fetch("https://" + web_site + ":8088" + "/get-info/",{
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token '+token.value
      },
    });

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);

      if(response.status == 401){
        token.value = null;
        localStorage.removeItem("auth-token");
        localStorage.removeItem("username");
      }
    }

    const data = await response.json() as {
      username: string,
      name: UserName,
      email: string,
      book_rate: number,
      institute_group: string,
      user_role: string,
      preferences: Preference[]
    };

    localStorage.setItem("username", data.username);
    username.value = data.username;

    console.log('Ответ от сервера +++++++++:', username.value);
    console.log('Ответ от сервера:', data);
    user_name.first_name = data.name.first_name;
    user_name.last_name = data.name.last_name;
    user_name.third_name = data.name.third_name;
    institute_group.value = data.institute_group;
    book_rating.value = data.book_rate;
    // user_preferences.value = data.preferences;

    const data_user_preferences = await data.preferences as Preference[];
    user_preferences.value = data_user_preferences;

    console.log('Предпочтения: ', user_preferences.value[0], user_preferences.value, data.preferences);
  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}

async function loadBBNumber(){
  try {
    const response = await fetch("https://" + web_site + ":8000/base-info/users_wallet/?username=" + username.value,{
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
    });

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);

      if(response.status == 401){
        token.value = null;
        localStorage.removeItem("auth-token");
        localStorage.removeItem("username");
      }
    }

    const data_number = await response.json() as BBNumber[];

    console.log('Ответ от сервера data_number[0].username:', data_number[0].username);
    number_bb.value = String(data_number[0].number_bb);

    console.log('Ответ от сервера header data_number:', data_number[0]);
    console.log('Ответ от сервера header username:', username);
    console.log('Ответ от сервера header number_bb:', number_bb);
    console.log('Ответ от сервера header username.value:', username.value);
    console.log('Ответ от сервера header number_bb.value:', number_bb.value);
    console.log('Ответ от сервера header admin_st2257:', 'admin_st2257');
  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}

async function loadInstituteGroup(){
  try {
    const response = await fetch("https://" + web_site + ":8088" + "/base-info/institute_group/",{
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
    });

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);
    }

    const data = await response.json() as InstituteGroup[];
    console.log('Ответ от сервера:', data);

    institute_groups.value = data;

  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}

async function loadPreferences(){
  try {
    const response = await fetch("https://" + web_site + ":8088" + "/base-info/preferences/",{
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token '+token.value
      },
    });

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);
    }

    const data = await response.json() as Preference[];
    console.log('Ответ от сервера:', data);

    preferences.value = data;

  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}

async function sendEditNameForm(){
  try {
    const response = await fetch("https://" + web_site + ":8088/edit_user_name/",{
      method: 'POST',
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: JSON.stringify({
        "type": "edit_user_name",
        "token": token.value,
        "first_name": form_first_name.value,
        "last_name": form_last_name.value,
        "third_name": form_third_name.value
      })
    });
    user_name.first_name = form_first_name.value ?? "Имя";
    user_name.last_name = form_last_name.value ?? "Фамилия";
    user_name.third_name = form_third_name.value ?? "Отчество";

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);
    }
    if (response.ok) {
        const data = await response.json();
        console.log('Ответ от сервера:', data);
        hidePopup();
        showNotification("name_notification");
        setTimeout(hideNotification, 2000, "name_notification");
    } else {
        console.error('Ошибка запроса:', response.status);
    }

  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}

async function sendEditGroupForm(){
  try {
    const response = await fetch("https://" + web_site + ":8088/edit_user_name/",{
      method: 'POST',
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: JSON.stringify({
        "type": "edit_user_group",
        "token": token.value,
        "group": selected_institute_group.value
      })
    });
    institute_group.value = selected_institute_group.value ?? "Имя";

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);
    }
    if (response.ok) {
        const data = await response.json();
        console.log('Ответ от сервера:', data);
        hidePopupEditGroup();
        // showNotification("name_notification");
        // setTimeout(hideNotification, 2000, "name_notification");
    } else {
        console.error('Ошибка запроса:', response.status);
    }

  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}

const showPopupRateInfo = ref(false);
const showPopup = ref(false);
const showEditGroup = ref(false);

const popupContentRateInfo = ref([
  '- Перед использоваем аудитории пользователь должен зарегистироваться в системе и забронировать аудитрию за выделенное ему число баллов бронирования, которые он может потратить на бронирвание аудитории в любое время (изначальный эквивалент одной пары - 1 балл бронирования)',
  '- Пользователь получает 28 баллов бронирования (дальше ББ) при регистрации',
  '- Каждый день пользователь получает в 0:00 +4ББ',
  '- При превышении числа 28, все баллы большие 28 сгорают',
  '- При заходе на сайт/телеграм приложение/мобильное приложение у пользователя есть возможность забронировать аудиторию на 1 или более пар по курсу ББ/пара, который установлен системой на текущее время',
  '- При бронировании аудитории пользователь можент забронировать выбранную из списка аудиторию или предложенную системой. При повторном бронировании пользователь может сохранить ту же аудиторию или выбрать новую',
  '- После окончания бронирвания в случае отсутствия заявки на бронирование на слудующую пару, аудитория считается свободной и подлежит свободному бронированию другими пользователями. После окончания бронирования пользователь должен привети аудиторию в изначальное состояние и покинуть аудиторию до начала сдеующего этапа бронирвания',
]);

const popupContent = ref([
  '- Перед использоваем аудитории пользователь должен зарегистироваться в системе и забронировать аудитрию за выделенное ему число баллов бронирования, которые он может потратить на бронирвание аудитории в любое время (изначальный эквивалент одной пары - 1 балл бронирования)',
  '- Пользователь получает 28 баллов бронирования (дальше ББ) при регистрации',
]);

const showPopupRateInfo_fun = () => {
  showPopupRateInfo.value = true;
};

const hidePopupRateInfo = () => {
  showPopupRateInfo.value = false;
};

const showPopup_func = () => {
  showPopup.value = true;
};

const hidePopup = () => {
  showPopup.value = false;
};


const showPopupEditGroup = () => { showEditGroup.value = true; };
const hidePopupEditGroup = () => { showEditGroup.value = false; };



    function showNotification(notificationId: string) {
      if (document.getElementById(notificationId)) {
        document.getElementById(notificationId)?.classList.add("show");
        document.getElementById(notificationId)?.classList.add("good_action");
      } else {
        console.error('Элемент с id "' + notificationId + '" не найден');
      }

    }

    function hideNotification(notificationId: string) {
      if (document.getElementById(notificationId)) {
        document.getElementById(notificationId)?.classList.remove("show");
        document.getElementById(notificationId)?.classList.add("good_action");
      } else {
        console.error('Элемент с id "' + notificationId + '" не найден');
      }
    }


async function sendAuthPost(){
  try {
    const response = await fetch("https://" + web_site + ":8088/oauth_yandex/",{
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        'access_token': "y0_AgAEA7qkNfKRAAymngAAAAEVhwM5AADyHiBoCChFpLOXWx4oCfaSrCdGmw"
      })
    });

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);
    }

    const data = await response.json();
    console.log('Ответ от сервера default_email:', data["Result"]["default_email"]);
    console.log('Ответ от сервера id:', data["Result"]["id"]);
    console.log('Ответ от сервера first_name:', data["Result"]["first_name"]);
    console.log('Ответ от сервера last_name:', data["Result"]["last_name"]);
    console.log('Ответ от сервера sex:', data["Result"]["sex"]);
  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
};

async function sendAuthGet(){
  try {

    const hash = window.location.hash;
    const queryString = new URLSearchParams(hash.slice(1));

    let access_token = queryString.get('access_token');
    token.value = access_token;
    console.log(access_token);

    const response = await fetch("https://" + web_site + ":8088/oauth_yandex/?access_token=" + access_token,{
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
    });

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);
    }

   const data = await response.json();
    console.log('Ответ от сервера default_email:', data["Result"]["default_email"]);
    console.log('Ответ от сервера id:', data["Result"]["id"]);
    console.log('Ответ от сервера first_name:', data["Result"]["first_name"]);
    console.log('Ответ от сервера last_name:', data["Result"]["last_name"]);
    console.log('Ответ от сервера sex:', data["Result"]["sex"]);
    console.log('Ответ от сервера sex:', data["token_for_user"]);

    localStorage.setItem("auth-token", data["token_for_user"]);
    console.log('========================', localStorage.getItem("auth-token"));
  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}

async function logAuth(){
  console.log('====');
  return "";
}

function selectOption(option: string) {
      selected_institute_group.value = option;
      search_institute_group.value = option;
}

</script>

<template>

<div style="padding-bottom: 70px;">
    <div class="centered-div">
        <div v-if="token == null">
            <h3>Для доступа в личный кабинет нужно авторизоваться</h3>
        </div>

        <template v-else>
            <Header />
                <!-- <div><p>Введенный текст: {{ form_first_name }} | {{ form_last_name }} | {{ form_third_name }} </p></div>-->
      
		<div class="class1" style="font-size: 24px;">
                    <div class="left-element" style="height: 100%">
                        <div style="width: 100%;">
				<span>{{user_name.first_name}}</span>
				<br class="half-line-break">
            		        <div class="full_name_div"></div>
	                        
				<span>{{user_name.third_name}}</span>
				<br class="half-line-break">
                                <div class="full_name_div"></div>
	                        
				<span>{{user_name.last_name}}</span>
                                <img class="icon-pic image_for_click" @click="showPopup_func" src="@/assets/edit.svg" alt="Edit">
                                <br>
                        </div>
          
		        <div style="position:absolute; bottom: 0; width: 100%">
                            <br>
                            <span>{{institute_group}}</span>
                            <img class="icon-pic image_for_click" src="@/assets/edit.svg" alt="Edit" @click="showPopupEditGroup">
                        </div>
                    </div>
        
		    <div class="right-element">
                        <img src="@/assets/2.jpg" class="profile-pic" style="width: 150px;" alt="Ваша фотография">
                    </div>
                </div>


                <div>
                    <div>
                        <p style="font-size: 24px;">Рейтинг бронирования: <img class="icon-pic image_for_click" @click="showPopupRateInfo_fun" src="@/assets/info.svg"></p>
                        <transition name="fade-rate-info">
                            <div v-if="showPopupRateInfo" class="popup">
                                <div class="popup-content">
                                    <button @click="hidePopupRateInfo" style="background-color: #dc3545;color: white;padding: 10px 20px;border: none;border-radius: 5px;cursor: pointer;">Закрыть</button>
                                    <p v-for="(line, index) in popupContentRateInfo" :key="index">{{ line }}</p>
                                    <button @click="hidePopupRateInfo" style="background-color: #dc3545;color: white;padding: 10px 20px;border: none;border-radius: 5px;cursor: pointer;">Закрыть</button>
                                </div>
                            </div>
                        </transition>
                    </div>

                    <div style="display: flex; justify-content: space-around">
                        <template v-for="index in 7">
                            <div class="star" :class="{checked : index <= book_rating}"></div>
                        </template>
                    </div>
                </div>

                <div>
                    <p style="font-size: 24px;">Баллы бронирования</p>
                    <span style="font-size: 18px;"> {{number_bb}} из 28 баллов</span><br>
                    <span style="color: grey; font-size: 12px;"> следующие +4 балла через 15 часов</span>
                </div>
                
		<div>
                    <div>
                        <p style="font-size: 24px;">Предпочтения:  <img class="icon-pic image_for_click" @click="showPopup_func" src="@/assets/edit.svg" alt="Edit"></p>
			<transition name="fade">
                            <div v-if="showPopup" class="popup">
                                <div class="popup-content">
                                    <h2>Редактирование ФИО</h2>

                                    <form @submit.prevent="sendEditNameForm">
                                        <input type="text" name="token" value="618b000cfdf0d5bd9402aff1b7e64ce9ec5e9d1a" hidden>
                                        <input type="text" name="type" value="edit_user_name" hidden>
                                        
					<div class="div-pop-up-edit-fio">
                                            <p style="font-size: 16px;padding: 10px;"><label for="first_name_input">Имя:</label></p>
                                            <p><input type="text" id="first_name_input" name="first_name" placeholder="Введите имя" v-model="form_first_name" /></p>
                                        </div>

                                        <div class="div-pop-up-edit-fio">
                                            <p style="font-size: 16px;padding: 10px;"><label for="last_name_input">Фамилия:</label></p>
                                            <p><input type="text" id="last_name_input" name="last_name" placeholder="Введите фамилию" v-model="form_last_name" /></p>
                                        </div>

                                        <div class="div-pop-up-edit-fio">
                                            <p style="font-size: 16px;padding: 10px;"><label for="third_name_input">Отчество:</label></p>
                                            <p><input type="text" id="third_name_input" name="third_name" placeholder="Введите отчество" v-model="form_third_name" /></p>
                                        </div>

                                        <div class="div-pop-up-edit-fio">
                                            <button @click="hidePopup" type="reset" style="background-color: #dc3545;color: white;padding: 10px 20px;border: none;border-radius: 5px;cursor: pointer;">Закрыть</button>
                                            <button type="submit" style="background-color: #4caf50; color: white;padding: 10px 20px;border: none;border-radius: 5px;cursor: pointer;">Сохранить</button>
                                        </div>
                                    </form>
	                        </div>
                            </div>
                        </transition>
                    </div>

                    <template v-for="preference in preferences">
                        <div style="font-size: 18px;">
                            {{preference.name}}
	                    <img class="icon-pic" :src="preferencesIcons[preference.name]" alt="">
                        </div>
                    </template>

		    <template v-for="preference in user_preferences">
                        <div style="font-size: 18px;">
                            {{preference.name}}
                            <img class="icon-pic" :src="preferencesIcons[preference.name]" alt="">
                        </div>
                    </template>

	  
		    <transition name="fade">
                            <div v-if="showEditGroup" class="popup">
                                <div class="popup-content">
					<h2>Выбор институтской группы</h2>
					<form @submit.prevent="sendEditGroupForm">
		    			    <div>	
						<input type="text" list="brow" placeholder="Введите название групп..." v-model="selected_institute_group"/>
						<datalist id="brow">
							<option v-for="option in institute_groups" :value="option.name">{{ option.name }}</option>
						</datalist>
		    			    </div>
					    <div class="div-pop-up-edit-fio">
					    	<button @click="hidePopupEditGroup" type="reset" style="background-color: #dc3545;color: white;padding: 10px 20px;border: none;border-radius: 5px;cursor: pointer;">Закрыть</button>
		    		            	<button type="submit" style="background-color: #4caf50; color: white;padding: 10px 20px;border: none;border-radius: 5px;cursor: pointer;">Установить группу</button>
				           </div>
					</form>
				</div>
                            </div>
                    </transition>

                </div>
      
	        <div style="padding-top: 10px;">
		    <button class="logout-button" @click="logout">Выйти</button>
		</div>
            </template>
        </div>

    	<div class="notification-container">
             <div class="notification" id="name_notification">
                <p>Вы успешно изменили ФИО</p>
                <span class="notification-close" @click="hideNotification('name_notification')">×</span>
            </div>
        </div>
    </div>
</template>


<style scoped>

.icon-pic {
  padding-left: 10px;
  width: 18px;
  float: right;
}


.star.checked {
  background: #F8CA00;
}

.star {
  display: inline-block;

  width: 32px;
  aspect-ratio: 1;
  background: #242424;
  clip-path: polygon(50% 0,
  calc(50%*(1 + sin(.4turn))) calc(50%*(1 - cos(.4turn))),
  calc(50%*(1 - sin(.2turn))) calc(50%*(1 - cos(.2turn))),
  calc(50%*(1 + sin(.2turn))) calc(50%*(1 - cos(.2turn))),
  calc(50%*(1 - sin(.4turn))) calc(50%*(1 - cos(.4turn)))
  );
  /* or more simple
  clip-path: polygon(50% 0,79% 90%,2% 35%,98% 35%,21% 90%);
   */
}

.profile-pic {
  border-radius: 32px;
}

.class1 {
  position: relative;
  height: 130px;
}

.container-head {
  position: relative; /* Позиционирование относительно контейнера */
  height: 100px; /* Высота контейнера (для демонстрации) */
}

.left-element, .right-element {
  position: absolute;
  top: 50%; /* Выравниваем по вертикали по центру */
  transform: translateY(-50%); /* Корректировка вертикального выравнивания */
}

.left-element {
  left: 0; /* Привязываем к левому краю */
}

.right-element {
  right: 0; /* Привязываем к правому краю */
}

.half-line-break {
  height: 0.5em;
}

.full_name_div {
	padding-top: 2px;
}


/*Базовые стили */
.logout-button {
  display: inline-block;
  padding: 10px 20px;
  background-color: #dc3545; /*Красный цвет */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

/*Стили при наведении курсора */
.logout-button:hover {
  background-color: #c82333; /*Более темный красный цвет */
}

/*Стили при нажатии */
.logout-button:active {
  background-color: #b0212b; /*Еще более темный красный цвет */
  transform: translateY(2px); /*Небольшой эффект нажатия */
}


.popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  z-index: 10;
}

.popup-content {
  max-height: 70vh; /*Adjust as needed */
  overflow-y: auto;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-active-rate-info,
.fade-leave-active-rate-info {
  transition: opacity 0.3s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-rate-info,
.fade-leave-to-rate-info {
  opacity: 0;
}

.close_button {
  background-color: #f44336; /* Red */
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}


@media (max-width: 768px) {
    .div-pop-up-edit-fio {
      width: 100%;
      display: flex;
      justify-content: space-between;
    }
    .popup-content{
      width: 80vw;
    }
}

@media (min-width: 768px) {
    .div-pop-up-edit-fio {
      width: 100%;
      display: flex;
      justify-content: space-between;
      }
      .popup-content{
        width: 30vw;
      }
}

  input[type="text"] {
    width: 100%;
    padding: 10px;
    margin-bottom: 5px;
    border: 1px solid #ccc;
    border-radius: 3px;
    box-sizing: border-box;
    /* Добавляем стили для input полей */
    font-size: 16px; /* Размер шрифта */
    color: #333; /* Цвет текста */
    background-color: #f5f5f5; /* Цвет фона */
    transition: all 0.3s ease; /* Плавный переход при наведении */
  }
  input[type="text"]:focus {
    outline: none; /* Убираем стандартное выделение */
    border-color: #4CAF50; /* Цвет границы при фокусе */
    box-shadow: 0 0 5px rgba(0, 150, 136, 0.2); /* Тень при фокусе */
  }


    .notification-container {
      position: fixed;
      top: 10px;
      right: 10px;
      z-index: 1000;
    }

    .good_action {
        background-color: #cfc;
    }

    .warning_action {
        background-color: #ffc;
    }

    .bad_action {
        background-color: #fcc;
    }

    .notification {
      border-radius: 5px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
      padding: 15px;
      margin-bottom: 10px; /*Отступ между уведомлениями */
      opacity: 0;
      transition: opacity 0.3s ease-in-out;
      display: none;
    }

    .notification.show {
      opacity: 1;
      display: block;
    }

    .notification-close {
      position: absolute;
      top: 10px;
      right: 10px;
      cursor: pointer;
    }

    .image_for_click{
        cursor: pointer;
    }

</style>
