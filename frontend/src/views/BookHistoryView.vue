<script setup lang="ts">

import BookTime from "@/components/book/BookTime.vue";
import Header from "@/components/TheHeader.vue";
import BookAmount from "@/components/book/BookAmount.vue";
import BookAudience from "@/components/book/BookAudience.vue";

import {ref, type Ref, onMounted, reactive, type Reactive, defineExpose, provide, inject} from 'vue';
import type {IAudience} from "@/classes/Interfaces";
import { useRouter } from 'vue-router';

interface BookItem {
  audience: string,
  user: string,
  number_bb: number,
  pair_number: number,
  date: string,
  booking_time: string
}

interface User {
    username: string;
}

interface AudienceItem {
    number: string;
    description: string;
    audience_status: string;
}

interface ActualBookItem {
  audience: AudienceItem,
  user: User,
  number_bb: number,
  pair_number: number,
  date: string,
  booking_time: string,
  time_slot: string
}

let actual_book_items: Ref<ActualBookItem[]> = ref([]);

// DO THIS
// const web_site = "mipt.site";
// const web_site = "localhost";
// const web_site = "127.0.0.1";
const web_site = inject('web_site');

const router = useRouter();

const time_slot_dict = [
    "09:00",
    "10:45",
    "12:20",
    "13:45",
    "15:30",
    "17:05",
    "18:35",
    "20:00",
    "22:00",
    "23:59",
    "01:30",
    "03:00",
    "04:30",
    "06:00"];

let book_history: Ref<BookItem[]> = ref([]);

let bookings: Ref<
      Array<{
        audience: IAudience,
        number_bb: Number,
        pair_number: Number,
        date: String,
        booking_time: String,
        user: {
          username: String
        }
      }>
    > = ref([]);

let username = ref<string|null>(null);
let token = ref<string|null>(null);
let start_time = ref<string|null>(null);
let end_time = ref<string|null>(null);

onMounted(()=>{
  token.value = localStorage.getItem("auth-token");
  username.value = localStorage.getItem("username");
  if(token.value == null) return;
  loadBookHistory();
  loadActualBookHistory();
});


async function loadActualBookHistory(){
  try {
    const response = await fetch("https://" + web_site + ":8000/base-info/book/?user=" + username.value,{
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
    });

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);

      if(response.status == 401){
        // token.value = null;
        localStorage.removeItem("auth-token");
        localStorage.removeItem("username");
      }
    }

    const data_number = await response.json() as ActualBookItem[];
    actual_book_items.value = data_number;
    
    start_time.value = time_slot_dict[Number(actual_book_items.value[0].time_slot) - 1];
    end_time.value = time_slot_dict[Number(actual_book_items.value[0].time_slot) + Number(actual_book_items.value[0].pair_number) - 1];
    
    // audiences_gk.value = data_number.filter(item => item.building.name == 'ГК');
    // audiences_lk.value = data_number.filter(item => item.building.name == 'ЛК');

    // username.value = data_number[0].username;
    // number_bb.value = String(data_number[0].number_bb);

    console.log('Ответ от сервера header actual_book_items:', actual_book_items);
    console.log('Ответ от сервера header book_history.value[0]:', book_history.value[0]);
  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}

async function action_Booking(audience_number: string, request_type: string){
  try {
    const response = await fetch("https://" + web_site + ":8000/stop_booking/",{
      method: 'POST',
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: JSON.stringify({
        "type": request_type,
        'token': token.value,
        'audience': audience_number // form_audience_name.value
      })
    });

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);
    }
    if (response.ok) {
        const data = await response.json();
        console.log('Ответ от сервера:', data);
    } else {
        console.error('Ошибка запроса:', response.status);
    }

  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}


async function loadBookHistory(){
  try {
    const response = await fetch("https://" + web_site + ":8000/base-info/history/?user=" + username.value,{
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
    });

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);

      if(response.status == 401){
        // token.value = null;
        localStorage.removeItem("auth-token");
        localStorage.removeItem("username");
      }
    }

    const data_number = await response.json() as BookItem[];
    book_history.value = data_number.reverse();


    // audiences_gk.value = data_number.filter(item => item.building.name == 'ГК');
    // audiences_lk.value = data_number.filter(item => item.building.name == 'ЛК');

    // username.value = data_number[0].username;
    // number_bb.value = String(data_number[0].number_bb);

    console.log('Ответ от сервера header data_number:', data_number);
    console.log('Ответ от сервера header book_history.value[0]:', book_history.value[0]);
  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}

  function showNotification_id(audience_number: string) {
      if (document.getElementById(String(audience_number))) {
        document.getElementById(String(audience_number))?.classList.add("show");
        document.getElementById(String(audience_number))?.classList.add("good_action");

        let array_id = ["date_", "time_", "number_", "pair_", "button_"];
        for (let i = 0; i < 5; i++) {
            if (document.getElementById(array_id[i] + String(audience_number))) {
                document.getElementById(array_id[i] + String(audience_number))?.classList.add("item_hidden");
            }
            else {
                console.error('Элемент с id "' + array_id[i] + audience_number + '" не найден');
            }
        }
      } else {
        console.error('Элемент с id "' + audience_number + '" не найден');
      }

      setTimeout(hideNotification, 2000, String(audience_number));
      setTimeout(router.go, 2000, 0);
    }

    function showNotification(notificationId: string) {
      if (document.getElementById(notificationId)) {
        document.getElementById(notificationId)?.classList.add("show");
      } else {
        console.error('Элемент с id "' + notificationId + '" не найден');
      }

    }

    function hideNotification(notificationId: string) {
      if (document.getElementById(notificationId)) {
        document.getElementById(notificationId)?.classList.remove("show");
      } else {
        console.error('Элемент с id "' + notificationId + '" не найден');
      }
    }


const showPopupAudBookingInfo = ref(false);
const showAudBookingInfo = () => { showPopupAudBookingInfo.value = true; };
const hideAudBookingInfo = () => { showPopupAudBookingInfo.value = false; };

</script>

<template>
  <div class="centered-div">
    <Header />

  </div>


 
    <div style="overflow-x: clip;" v-for="actual_item in actual_book_items" :id="`tr_${actual_item.audience.number}`" class="container">
        <div class="auditorium">
            <div class="details">
		<span><h3>Аудитория {{actual_item.audience.number}} ГК</h3></span>
            	<span><img @click="showAudBookingInfo()" class="icon-pic image_for_click" src="@/assets/info.svg"></span>
	    </div>

	    <div class="details"><span>Дата: <strong>{{actual_item.date}}</strong></span></div>
	    <div class="details"><span>Время бронирования: <strong>{{actual_item.booking_time.slice(0, 8)}}</strong></span></div>
            <div class="details"><span>Аудитория: <strong>{{actual_item.audience.number}} ГК</strong></span></div>
	    <div class="details"><span>Пар для бронирования: <strong>{{actual_item.pair_number}} шт.</strong></span></div>
	    <div class="details">
		    <span>Начало: <strong>{{ start_time }}</strong></span>
		    <span>Конец: <strong>{{ end_time }}</strong></span>
            </div>
            <div style="flex-wrap: wrap; display: flex; gap: 1vw;">
				<button @click="action_Booking(actual_item.audience.number, 'cancel_booking');showNotification_id(actual_item.audience.number);" class="button" style="width: 20vw; background-color: #DC3545;">Отменить</button>
				<button @click="action_Booking(actual_item.audience.number, 'finalize_booking');showNotification_id(actual_item.audience.number);" class="button" style="width: 20vw; background-color: #FFAB42;">Завершить</button>
				<button @click="action_Booking(actual_item.audience.number, 'not_my_booking');showNotification_id(actual_item.audience.number);" class="button" style="width: 50vw; background-color: #203979;">Аудитория занята не мной</button>
            <button @click="action_Booking(actual_item.audience.number, 'this_is_my_booking');showNotification_id(actual_item.audience.number);" class="button" style="width: 92vw;">Ура, я в аудитории</button>
        	</div>
        </div>
    </div>

    <h2>История бронирования</h2>
    <div style="padding-bottom: 70px;">
    <table class="booking-table" style="padding-bottom: 70px;">
      <thead>
        <tr>
          <th>Дата</th>
          <th>Время</th>
          <th>Комната</th>
          <th>Номер пары</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="book in book_history">
          <td>{{book.date}}</td>
          <td>{{book.booking_time.slice(0, 8)}}</td>
          <td>{{book.audience}}</td>
          <td>{{book.pair_number}}</td>
        </tr>
      </tbody>
    </table>
    </div>

  <div class="notification-container">
      <div v-for="actual_item in actual_book_items">
        <div class="notification" :id="actual_item.audience.number">
          <p>Бронирование аудитории {{actual_item.audience.number}} завершено</p>
          <span class="notification-close" @click="hideNotification(actual_item.audience.number)">×</span>
        </div>
      </div>
  </div>


	<transition name="fade-rate-info">
  	<div v-if="showPopupAudBookingInfo" class="popup button-width button-width">
        	<div class="popup-content">
                	<p>
                                <a href="https://mipt.site/info">ПОДРОБНЕЕ ТУТ</a>
                        </p>

			<div v-for="actual_item in actual_book_items">
                            <p>
				Вы забронировали аудиторию {{actual_item.audience.number}} ГК. Бронирование не означает гарантированное нахождение в аудиории
				одному. Сервис позволяет экономить время за счёт автоматической подгрузки занятых аудиторий. Некоторые пары, указанные в 
				брониронии учебного управления не отображаются в системе из-за постоянно меняющегося расписания.
                            </p>
                            <p>
                                Предпотения пользоватея позволяют бронировать аудитории совместно для уплотнения студентов и более эффективной и
				качественной работы в коллективе.
                            </p>
			    <p>
                                В случае, если аудитория занята нажмите: "АУДИТОРИЯ ЗАНЯТА НЕ МНОЙ" - и сервис предоставит одну из резервных аудиторий.
                            </p>
			    <p>
                                Уведомляем о том, что бронирование на определенное время может быть недоступно из-за высокой стоимости пары
				в Баллах Бронирования. Данная система позволяет бронировать аудитории вне зависимости от того, кто 
				первым занял аудиторию.
                            </p>
			</div>

                        <button @click="hideAudBookingInfo" style="background-color: #dc3545; width: 100%;  color: white;padding: 10px 20px;border: none;border-radius: 5px;cursor: pointer;">Закрыть</button>
               </div>
        </div>
	</transition>



</template>

<style scoped>

@media (max-width: 768px) {
        .button-width {
                min-width: 80vw;
        }
}

@media (min-width: 768px) {
        .button-width {
                max-width: 30vw;
        }
}

.table {
  display: flex;
}

.table-header {

}

    .booking-history {
      width: 80%;
      margin: 20px auto;
      border: 1px solid #ccc;
      border-radius: 5px;
      padding: 20px;
    }

    .booking-history h2 {
      margin-top: 0;
    }

    .booking-table {
      max-width: 100vw;
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
    }

    .booking-table th,
    .booking-table td {
      border: 1px solid #ccc;
      padding: 10px;
      text-align: left;
    }

    .booking-table th {
      background-color: #f2f2f2;
      font-weight: bold;
    }
.cancel-button {
  display: inline-block;
  padding: 8px 12px;
  background-color: #dc3545; /*Красный цвет */
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.cancel-button:hover {
  background-color: #c82333; /*Более темный красный цвет */
}

.cancel-button:active {
  background-color: #b0212b; /*Еще более темный красный цвет */
  transform: translateY(2px); /*Эффект нажатия */
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

    .item_hidden{
        visibility: hidden;
    }

        body {
            font-family: sans-serif;
        }

        .container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            padding: 0px;
        }

        .auditorium {
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 5px;
            margin-bottom: 20px;
            width: 92vw;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        .auditorium h3 {
            margin-top: 0;
        }

        .auditorium .details {
            display: flex;
            justify-content: space-between;
        }

        .auditorium .details span {
            font-size: 14px;
            color: #666;
        }

        .auditorium .details strong {
            font-weight: bold;
        }

        .auditorium .button {
            display: block;
            background-color: #4CAF50;
            color: white;
            padding-top: 10px;
	    padding-bottom: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 14px;
            margin-top: 10px;
        }

        .auditorium .button:hover {
            background-color: #45a049;
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


.icon-pic {
  width: 18px;
  float: right;
  border: 3px solid #ccc;
  border-radius: 10px;
  padding-left: 10px;
  padding-right: 10px;
}

.image_for_click{
  cursor: pointer;
}


</style>
