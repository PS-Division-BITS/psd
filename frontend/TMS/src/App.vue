<template>
<div>
  
  <v-app>

    <Header/>
    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</div>
</template>

<script>
import Header from './components/Header'
export default {
  name: 'App',

  components: {
   Header
    
  },

  data: () => ({
    //
  }),
};
</script>
