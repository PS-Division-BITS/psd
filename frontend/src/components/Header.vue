<template>
    <div>
      <v-app-bar
     app

      color="grey lighten-4"
      dark
      class="px-0 mx-0"
      height="100"
      flat
    >

      <v-img src="@/assets/ps_logo.gif" contain aspect-ratio max-width="400" ></v-img>
      <LoggedInUserDisplay />  
      <UserProfileEditDialog />
    </v-app-bar>
    </div>
</template>
<script>
import LoggedInUserDisplay from "./LoggedInUserDisplay";
import UserProfileEditDialog from "./UserProfileEditDialog";
export default {
  name:"Header",
  components:{
    UserProfileEditDialog,
    LoggedInUserDisplay
  }
}
</script>