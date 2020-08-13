<template>
 <div class="ml-auto">
   <v-row>
     <v-dialog v-model="dialog" persisitent max-width="1000px">
      <template v-slot:activator="{on,attrs}">
        <v-btn color="primary" dark v-bind="attrs" v-on="on">
        Edit User Profile
        </v-btn>
      </template>
      <v-card>
        <v-card-title justify="center">
          <span class="headline">User Profile</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" v-for="field in fields" :key="field.id">
                <v-text-field :label="field.name" required></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
         <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialog = false">Close</v-btn>
          <v-btn color="blue darken-1" text @click="dialog = false">Save</v-btn>
        </v-card-actions>
      </v-card>
     </v-dialog>
   </v-row>
 </div>
</template>
<script>
export default {
  name:"UserProfileEditDialog",
  data(){
    return{
        dialog:false,
      fields:[
        {
          id:1,
          name:"First Name*",
          required:true
        },
        {
          id:2,
          name:"Middle Name"
        },
        {
          id:3,
          name:"Last Name*",
          required:true
        },
        {
          id:4,
          name:"ID",
          required:true
        },
        {
          id:5,
          name:"Email*",
          required:true
        },
        {
          id:6,
          name:"CGPA(last semester)"

        },
        {
          id:7,
          name:"Address"
        },
        {
          id:8,
          name:"Phone Number*",
          required:true
        }
      ]
        
  }
  
 }
}
</script>
<style scoped>
</style>
