<template>
   <div>
     <v-app-bar
      color='indigo'
      dark    
    >
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title class="ml-auto"> <span class="font-weight-light">PS Admin</span> Dashboard <span>  </span></v-toolbar-title>
    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      absolute
      
      class="grey lighten-3"
    >
      <!-- <v-list
        nav
        dense
      >
        <v-list-item-group
          v-model="drawer"
          active-class="blue--text text--accent-4"
        >
        
          <v-list-item>
            <v-list-item-title>Services</v-list-item-title>
          </v-list-item>

         

        </v-list-item-group>
      </v-list> -->
       <v-list-item-group
          active-class="blue--text h5 text--accent-4"
        >
        <v-list nav dense v-for="link in links" :key="link.text" >
             
              <v-list-item router :to="{name:link.route}">
                  <v-list-item-action>
                      <v-icon>{{link.icon}}</v-icon>
                  </v-list-item-action>
                  <v-list-item-content>
                      <v-list-item-title >{{link.text}}</v-list-item-title>
                  </v-list-item-content>

           </v-list-item>
              
          </v-list>
       </v-list-item-group>
    </v-navigation-drawer>
     
    <v-container >
      <router-view/>
    </v-container>
        
    
  </div>
</template>
<script>
export default {
    name:"Dashboard",
    data(){
        return{
            drawer:true,
            links : [
              {
                text:'Services',
                icon : 'mdi-cogs',
                route : 'Admin.Services'
              },
              {
                text:'Users',
                icon : 'mdi-account-group',
                route : 'Admin.Users'
              },
              {
                text:'Groups',
                icon : 'mdi-group',
                route : 'Admin.Groups'
              }
            ]
        }
    },
   
    mounted ()
    {
     
    }    
}
</script>
<style scoped>

</style>