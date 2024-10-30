<script setup lang="ts">
import {ref, onUpdated} from "vue";

const emit = defineEmits<{
  (e: "select-amount", amount: Number):void
}>()

let amount = ref<Number>(1);

function emitSelect(){
  emit('select-amount', amount.value);
}

const showPopupPairNumberInfo = ref(false);
const showPairNumberInfo = () => { showPopupPairNumberInfo.value = true; };
const hidePairNumberInfo = () => { showPopupPairNumberInfo.value = false; };

</script>

<template>
          <div class="container-head" style="height: 60px;">
                <div class="left-element">
                        <h3>Количество пар</h3>
                </div>

                <div class="right-element">
                        <img @click="showPairNumberInfo" class="icon-pic image_for_click" src="@/assets/info.svg">
                </div>
          </div>


	  <!-- <h3>Количество пар</h3> -->
  <output>1</output>
  <input type="range" value="1" min="1" max="6" style="width: 80%;"
         v-model="amount" @input="emitSelect" required>
  <output>6</output><br><br>


        <transition name="fade-rate-info">
                <div v-if="showPopupPairNumberInfo" class="popup button-width">
                    <div class="popup-content">
			    <!-- <button @click="hidePairNumberInfo" type="reset" style="background-color: #dc3545; width: 100%;  color: white;padding: 10px 20px;border: none;border-radius: 5px;cursor: pointer;">Закрыть</button> -->

			    <p>
			    	За один раз пользователь может забронировать не более 6-ти пар. По умоланию пользователь бронирует одну пару. 
			    </p>

                        <button @click="hidePairNumberInfo" type="reset" style="background-color: #dc3545; width: 100%;  color: white;padding: 10px 20px;border: none;border-radius: 5px;cursor: pointer;">Закрыть</button>
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

input[type=range] {
  -webkit-appearance: none;
  width: 200px;
  height: 8px;
  background: #ddd;
  outline: none;
  border-radius: 10px;
/*Добавляем тень для полосы ползунка */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #4CAF50;
  cursor: pointer;
  /*Добавляем тень для ползунка */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

input[type=range]::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #4CAF50;
  cursor: pointer;
  /*Добавляем тень для ползунка (Firefox) */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
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
