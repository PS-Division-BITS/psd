
import ServicesList from '../components/Admin/ServicesList'
import Users from '../components/Admin/Users'


const admin_routes = [
    
    {
      path : 'services',
      name : 'Admin.Services',
      component :  ServicesList,    
      meta : {
            title : 'PS Admin | Services',
            
        }
    },

    {
        path : 'users',
        name : 'Admin.Users',
        component : Users,
        meta : {
            title : 'PS Admin | User List'
        }
    },

    {
        path : 'groups',
        name : 'Admin.Groups',
       
    }
]

export default admin_routes