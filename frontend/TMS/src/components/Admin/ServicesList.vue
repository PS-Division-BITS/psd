<template>
    <v-container grid-list-xs>
       
       <v-row>
           <v-col cols="12" md="6" v-for ="(app,index) in apps" :key=index>
         <v-card>
             <v-card-subtitle>
                 <div class="headline text--primary">{{app.name}}</div>
             </v-card-subtitle>
             
             <v-card-text>
                <v-text-field
                    name="deadline"
                    label="Deadline"
                   
                    v-model="app.deadline"
                ></v-text-field>
             <div class="d-flex justify-space-between align-center">
                <v-switch  label="Service Status" v-model="app.status"></v-switch>
                
              
                <span v-if="app.users">Total Users : {{app.users}} </span>
             </div>
             </v-card-text>

             <v-card-actions class="justify-center">
                 <v-btn small color="primary">Update Config</v-btn>
             </v-card-actions>
         </v-card>
           </v-col>
       </v-row>
    </v-container>
</template>

<script>
export default {
    data : function() {
        return  {
            apps : [
                {
                    name : 'Transfer Management System',
                    deadline : '15th August, 2020',
                    url : '',
                    status : true,
                    users : '999',
                    id : 1
                },
                {
                    name : 'Complaint Management System',
                    deadline : '15th August, 2020',
                    url : '',
                    status : false
                },
                {
                    name : 'Leave Management System',
                    deadline : '15th August, 2020',
                    url : '',
                    status : false
                },
                {
                    name : 'App1',
                    deadline : '15th August, 2020',
                    url : '',
                    status : false
                }
            ]
        }
    }
}
</script>