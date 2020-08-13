<template>
<div>
       <v-row class="black--text ml-auto" v-if="user.loggedIn">
         <div class="headline">{{user.name}} {{user.profile}}</div>
         <div></div>
       </v-row>
</div>
</template>
<script>
export default {
    name:"LoggedInUserDisplay",
    data(){
        return{
           
            user:{
                loggedIn:true,
                name:"Username",
                profile:"ProfileName"//This corresponds to whether the user is a student or faculty or whatever
            }
        }
    }
}
</script>