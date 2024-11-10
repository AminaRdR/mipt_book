<script setup lang="ts">

import Header from "@/components/TheHeader.vue";
import {ref, type Ref, onMounted, reactive, type Reactive, defineExpose, provide, inject} from 'vue';
import { useRouter } from 'vue-router';

interface Pair {
  name: string,
  time_slot_index: number,
  week_day_index: number,
  description: string,
}

interface SearchItem {
  name: string,
  description: string,
  pair: Pair,
  owner_user_wallet: string,
}

// DO THIS
// const web_site = "mipt.site";
// const web_site = "localhost";
// const web_site = "127.0.0.1";
const web_site = inject('web_site');

const router = useRouter();

let token = ref<string|null>(null);
let username = ref<string|null>(null);
let search_data: Ref<SearchItem[]> = ref([]);
let search_text = ref<string|null>(null);

onMounted(()=>{
  token.value = localStorage.getItem("auth-token");
  username.value = localStorage.getItem("username");
  // loadSearch("Б02-");
});


async function loadSearch(){
  try {
    const response = await fetch("https://" + web_site + ":8000/base-info/event_item/?search_text="+search_text.value,{
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
    });

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);

      if(response.status == 401){
        localStorage.removeItem("auth-token");
      }
    }

    const data_number = await response.json() as SearchItem[];
    search_data.value = data_number;

    console.log('Ответ от сервера header data_number:', data_number);
  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}


</script>

<template>
<div>
    <h1>Поиска:</h1>
        <form @submit.prevent="loadSearch">
            <input type="text" id="scales" name="scales" v-model="search_text"/>
            <button type="submit"><h3>Искать</h3></button>
		</form>
</div>

<div>
    <h1>Результат поиска:</h1>
    <template v-for="search_item in search_data">
	    <div style="padding-top: 10px;">
            <p>Мероприятие: {{search_item.name}}</p>
            <p>Описание: {{search_item.description}}</p>
            <p>Владелец: {{search_item.owner_user_wallet}}</p>
            <p>Пара: {{search_item.pair.name}}</p>
            <p>Временной слот: {{search_item.pair.time_slot_index}}</p>
            <p>День недели: {{search_item.pair.week_day_index}}</p>
            <p>Описание пары: {{search_item.pair.description}}</p>
        </div>
    </template>
</div>

</template>

<style scoped>
</style>
