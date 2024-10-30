<script setup lang="ts">
import {ref, onMounted, provide, inject} from 'vue';
import type {IBuilding, IAudience} from "@/classes/Interfaces";

const emit = defineEmits<{
  (e: 'select-audience', arg: IAudience) : void
}>();

// DO THIS
// const web_site = "mipt.site";
// const web_site = "localhost";
// const web_site = "127.0.0.1";
const web_site = inject('web_site');

let is_random_selected = ref<Boolean>(false);
let building_arr = ref<Array<IBuilding>>([]);
let audience_arr = ref<Array<IAudience>>([]);

let building_name_selected = ref<String>("");
let audience_number_selected = ref<String>("");

onMounted(async () =>{
  let web_address = '/backend-api';
  let building_path = '/base-info/building/?institute=%D0%9C%D0%A4%D0%A2%D0%98';
  let audience_path = '/base-info/audience/?institute=%D0%9C%D0%A4%D0%A2%D0%98&status=%D0%A1%D0%B2%D0%BE%D0%B1%D0%BE%D0%B4%D0%BD%D0%BE';

  //building_arr.value = await getInfo(web_address+building_path);
  //audience_arr.value = await getInfo(web_address+audience_path);
  building_arr.value = await getInfo('https://' + web_site + ':8000'+building_path);
  audience_arr.value = await getInfo('https://' + web_site + ':8000'+audience_path);
  setTimeout(setDefault, 500, 0);
});

function setDefault() {
    building_name_selected.value = building_arr.value[0].name;
    audience_number_selected.value = audience_arr.value[0].number;
    emit('select-audience',  audience_arr.value[0]);
}

async function getInfo(url: string){
  try {
    const response = await fetch(url,{
      method: 'GET',
      headers: {'Content-Type': 'application/json'},
    });

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);
    }

    const data = await response.json();
    console.log('Ответ от сервера:', data);
    return data;

  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}

function selectAudience(audience: IAudience | null){
  if (!audience) return;
  audience_number_selected.value = audience.number;
  is_random_selected.value = false;
  emit('select-audience', audience);
}

function selectBuilding(building: IBuilding){
  building_name_selected.value = building.name;
  is_random_selected.value = false;
  audience_number_selected.value = "";
}

function selectRandom(){
  let audiences_sel_building : IAudience[] = [];

  for(let key in audience_arr.value){
    let cur_item = audience_arr.value[key];
    if (cur_item.building.name != building_name_selected.value) continue;
    audiences_sel_building.push(cur_item);
  }

  let random_audience = audiences_sel_building[Math.floor(Math.random()*audiences_sel_building.length)];
  selectAudience(random_audience);
  is_random_selected.value = true; // it's important to place it after selecting;
}

const showPopupAudNumberInfo = ref(false);
const showAudNumberInfo = () => { showPopupAudNumberInfo.value = true; };
const hideAudNumberInfo = () => { showPopupAudNumberInfo.value = false; };


</script>

<template>
	<div class="container-head" style="height: 60px;">
        	<div class="left-element">
			<h3>Номер аудитории</h3>
        	</div>
        	
		<div class="right-element">
          		<img @click="showAudNumberInfo" class="icon-pic image_for_click" src="@/assets/info.svg">
        	</div>
      </div>
      <!-- <h3>Номер аудитории</h3>-->
  

  <div class="container">
    <template v-for="building in building_arr" :key="building.name">
      <div class="item button" :class="{selected: building.name== building_name_selected}" @click="selectBuilding(building)"> {{building.name}} </div>
    </template>
  </div>
  <div class="container">
    <div class="item button" :class="{ selected: is_random_selected }" @click="selectRandom()">Случайная</div>
    <template v-for="audience in audience_arr" :key="audience.number">
      <div v-if="audience.building.name == building_name_selected" class="item button"
           :class="{ selected: audience.number == audience_number_selected }" @click="selectAudience(audience)"> {{audience.number}} {{audience.building.name}} </div>
    </template>
  </div>

        <transition name="fade-rate-info">
                <div v-if="showPopupAudNumberInfo" class="popup button-width">
                    <div class="popup-content">
			    <!-- <button @click="hideAudNumberInfo" type="reset" style="background-color: #dc3545; width: 100%;  color: white;padding: 10px 20px;border: none;border-radius: 5px;cursor: pointer;">Закрыть</button> -->

                        <p>
				В тестовом режиме доступно бронирование аудиторий на 4-м и 5-м этажах ГК.
				Бронирование возможно в свободное от запланированных учебным управлением
				временные слоты. Подробнее загруженность аудиторий можно посмотреть: 
				<a href="https://mipt.site/display/">здесь</a>
			</p>

                        <button @click="hideAudNumberInfo" type="reset" style="background-color: #dc3545; width: 100%;  color: white;padding: 10px 20px;border: none;border-radius: 5px;cursor: pointer;">Закрыть</button>
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


.button {
  background-color: white;
  border: none;
  cursor: pointer;
  color: black;
}

.selected, .selected.button {
  background-color: lightblue;
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
