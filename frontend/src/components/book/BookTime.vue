<script setup lang="ts">
import {onMounted, ref} from 'vue'

// setup selected time slot
const emit = defineEmits<{
  (e: "select-time-slot", time_slot: String):void
}>()

function emitSelect(){
  emit('select-time-slot', String(formatTime(selected_time.value)));
}


function fDate(hours : number, minutes : number){
  // short for factoryDate
  let out = new Date();
  out.setHours(hours); out.setMinutes(minutes)
  if (hours < 8) { // hardcoded nonsense
    out.setDate(out.getDate()+1);
  }
  return out;
}

function getDefaultTime(){
  for(let i = 0; i<times.value.length ; i++){
    if(!isOld(times.value[i])) return times.value[i];
  }
  return times.value[0];
}

let times = ref([
  fDate(9,0),  fDate(10,45), fDate(12,20), fDate(13,45), fDate(15,30),
  fDate(17,5), fDate(18,35), fDate(20,0),  fDate(22,0),  fDate(23,59),
  fDate(1,30), fDate(3,0),   fDate(4,30),  fDate(6,0),
])

let selected_time = ref<Date>(new Date());

onMounted(()=>{
    selected_time.value = getDefaultTime();
    emitSelect();
});

function isOld(date : Date){
  let now = new Date();
  // console.log("====" + String(now.getTime()) + "====" + String(date.getTime()));
  let result = now.getTime() > date.getTime();
  return result;
}
function formatTime(date: Date){
  return date.toLocaleTimeString("ru-RU", {hour: "2-digit", minute: "2-digit"});
}

function selectTime(time: Date){
  // emitSelect();
  if(isOld(time)) return;
  selected_time.value = time;
  emitSelect();
  // console.log(String(selected_time.value));
}

const showPopupTimeSlotInfo = ref(false);
const showTimeSlotInfo = () => { showPopupTimeSlotInfo.value = true; };
const hideTimeSlotInfo = () => { showPopupTimeSlotInfo.value = false; };

</script>

<template>
          <div class="container-head" style="height: 60px;">
                <div class="left-element">
                        <h3>Время начала бронирования</h3>
                </div>

                <div class="right-element">
                        <img @click="showTimeSlotInfo" class="icon-pic image_for_click" src="@/assets/info.svg">
                </div>
          </div>

	  <!-- <h3>Время начала бронирования</h3> -->
  

  <div class="time-selector" id="timeSelector">
    <template v-for="time in times">
      <div  class="time-option"
           :class="{selected: time.getTime() == selected_time.getTime()}"
           @click="selectTime(time)"
            v-if="!isOld(time)"
      >{{formatTime(time)}}</div>
    </template>
  </div>


        <transition name="fade-rate-info">
                <div v-if="showPopupTimeSlotInfo" class="popup button-width">
                    <div class="popup-content">
			    <!-- <button @click="hideTimeSlotInfo" type="reset" style="background-color: #dc3545; width: 100%;  color: white;padding: 10px 20px;border: none;border-radius: 5px;cursor: pointer;">Закрыть</button> -->

                        <p>
				Доступные временные слоты для бронирования подгружаются на основе расписания и уже существующих бронирований.
				Время бронирования привязано к парам. Разбивка времени после 20:00 определена севисом и согласована с администрацией.
			</p>

                        <button @click="hideTimeSlotInfo" type="reset" style="background-color: #dc3545; width: 100%;  color: white;padding: 10px 20px;border: none;border-radius: 5px;cursor: pointer;">Закрыть</button>
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

.time-selector {
  width: 100%;
  overflow: scroll;
}

.time-option {
  display: inline-block;
  padding: 5px 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-right: 10px;
  margin-top: 10px;
  cursor: pointer;
}

.time-option.selected {
  background-color: lightblue;
}

.time-option.old.selected {
  background-color: #5a6971;
}

.time-option.old {
  background-color: #5a6971;
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
