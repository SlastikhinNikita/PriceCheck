

// register the grid component
Vue.component('demo-grid', {
    template: '#grid-template',
    props: {
        heroes: Array,
        columns: Array,
        filterKey: String,
		selected: ''
    },
    data: function() {
        var sortOrders = {}
        this.columns.forEach(function(key) {
            sortOrders[key] = 1
        })
        return {
            sortKey: '',
            sortOrders: sortOrders
        }
    },
    computed: {
        filteredHeroes: function() {
            var sortKey = this.sortKey
//         var filterKey = this.filterKey && this.filterKey.toLowerCase()
            var order = this.sortOrders[sortKey] || 1
            var heroes = this.heroes
/*            if (filterKey) {
                heroes = heroes.filter(function(row) {
                    return Object.keys(row).some(function(key) {
                        return String(row[key]).toLowerCase().indexOf(filterKey) > -1
                    })
                })
            }*/
            if (sortKey) {
                heroes = heroes.slice().sort(function(a, b) {
                    a = a[sortKey]
                    b = b[sortKey]
                    return (a === b ? 0 : a > b ? 1 : -1) * order
                })
            }
            return heroes
        }
    },
    filters: {
        capitalize: function(str) {
            return str.charAt(0).toUpperCase() + str.slice(1)
        }
    },
    methods: {
        sortBy: function(key) {
            this.sortKey = key
            this.sortOrders[key] = this.sortOrders[key] * -1
        },
		
		clickOnMain: function(element) {
			this.selected = element.id;
			demo.selected = this.selected;
			demo3.selected = this.selected;
			var arr = demo3.gridData;
			for (el in arr){
				arr[el].forEach(function(entry) {
				entry.diff = entry.price - element.price;
			});
			}
		},
		delRow: function(element) {
			var arr = demo.gridData;

			for( var i = 0; i < arr.length; i++){ 
			   if ( arr[i].id === element.id) {
				 arr.splice(i, 1); 
			   }
			}
			
		}
		
    }
})



var control = new Vue({

    el: '#control',
    data: {
        searchQuery: '',
        searchQuery2: '',
        searchQuery3: '',
        gridColumns: ['del', 'id', 'name', 'price'],
        gridData: [],
		selected: '',
        searchQueryList: []  
    },
    methods: {
        updateGrid: function(key) {
            if (this.searchQuery.length > 4) {
                var dataURL = '/api/1.0/get_main_table';
                dataURL = dataURL + '?query=' + this.searchQuery;
				axios
                     .get(dataURL)
                     .then(response => (demo.gridData = response.data));
            }
        },
		initSearchQueryList: function(){
				var dataURL = '/api/1.0/read_searchquery';

				axios
					.get(dataURL)
					.then(response => (demo.searchQueryList = response.data));	
		},
		createSearchQuery: function(){
			    var dataURL = '/api/1.0/create_searchquery';

                dataURL = dataURL + '?query=' + demo.searchQuery;
				axios
                     .post(dataURL);
				this.initSearchQueryList();
		},		
		getAllComp: function() {
			    var dataURL3 = '/api/1.0/get_comp_table_all';
                dataURL3 = dataURL3 + '?query=' + control.searchQuery2 + '&second=' + control.searchQuery3;
				axios
                     .get(dataURL3)
                     .then(response => (demo3.gridData = response.data))
					 .then(demo3.visible=true);
		}

    },
	mounted () {
		this.gridData[0] = ''
		this.initSearchQueryList()
 
	},	
	
})



var demo = new Vue({

    el: '#demo',
    data: {
        searchQuery: 'Введите минимум 5 символов',
        gridColumns: ['del', 'id', 'name', 'price'],
        gridData: [],
		selected: '',
        searchQueryList: []  
    },
    methods: {
        updateGrid: function(key) {
            
                var dataURL = '/api/1.0/get_main_table';
                var self = demo;
                dataURL = dataURL + '?query=' + demo.searchQuery;
				axios
                     .get(dataURL)
                     .then(response => (demo.gridData = response.data));
            
        },
		clearSearch: function() {
			document.getElementById("searchinput").value = ""; 
			//demo.searchQuery = ''
		},

		initSearchQueryList: function(){
				var dataURL = '/api/1.0/read_searchquery';

				axios
					.get(dataURL)
					.then(response => (demo.searchQueryList = response.data));	
		},
		createSearchQuery: function(){
			    var dataURL = '/api/1.0/create_searchquery';

                dataURL = dataURL + '?query=' + demo.searchQuery;
				axios
                     .post(dataURL);
				this.initSearchQueryList();
		}


    },
	mounted () {
		this.gridData[0] = ''
		this.initSearchQueryList()
 
	},	
	
})









Vue.component('demo-grid3', {
    template: '#grid-template3',
    props: {
        comp_name: Object,
        columns: Array,
		visible: false
    },
    data: function() {
        var sortOrders = {}
        this.columns.forEach(function(key) {
            sortOrders[key] = 1
        })
        return {
            sortKey: '',
            sortOrders: sortOrders
        }
    },
    computed: {
        filteredHeroes: function() {
            var sortKey = this.sortKey
            var order = this.sortOrders[sortKey] || 1
            var comp_name = this.comp_name
			console.log(comp_name);
            if (sortKey) {
                comp_name = comp_name.slice().sort(function(a, b) {
                    a = a[sortKey]
                    b = b[sortKey]
                    return (a === b ? 0 : a > b ? 1 : -1) * order
                })
            }
            return comp_name
        }
    },
    filters: {
        capitalize: function(str) {
            return str.charAt(0).toUpperCase() + str.slice(1)
        }
    },
    methods: {
        sortBy: function(key) {
            this.sortKey = key
            this.sortOrders[key] = this.sortOrders[key] * -1
			console.log(key);
        },
		delRow: function(element) {
			//element.id;
			var arr = demo3.gridData;

			for (el in arr){
				arr[el].forEach(function(entry, index, object) {
					if (entry.id === element.id){
						object.splice(index, 1);
					}
				
			});
			}
			for( var i = 0; i < arr.length; i++){ 
			   if ( arr[i].id === element.id) {
				 arr.splice(i, 1); 
			   }
			}
			
		}
    }
})




var demo3 = new Vue({
    el: '#demo3',
    data: {
        gridColumns: ['del', 'id', 'name', 'price','diff'],
//        gridData: [],
		selected: '',
		visible: false,	
        gridData: Object({"f":""})
    },
    methods: {

	}
	
	
})





var SaveResultButton = new Vue({
    el: '#SaveResultButton',
    data: {
		selected: ''
    },
    methods: {

		saveResult: function(){
			var mainArray = [];
			var compArray = [];
			var arr = demo.gridData;
			arr.forEach(function(entry) {
			mainArray.push(entry.id);
			});

			var arr = demo3.gridData;
			for (el in arr){
				arr[el].forEach(function(entry) {
				compArray.push(entry.id);
			});
			}
			if (demo3.selected == '') {
				alert('Вы не выбрали запись');
			}	
			else {
		    var dataURL = '/api/1.0/create_result';
            dataURL = dataURL + '?selected=' + demo3.selected + "&mainrecord=" + mainArray + "&comprecord=" + compArray;

			if (axios.post(dataURL)){	
			alert('Запись отправлена на сохранение');
			}
		}}
	}
	
	
})


Vue.component('modal', {
  template: '#modal-template'
})

// start app
new Vue({
  el: '#app',
  data: {
    showModal: false,
	priceNamesList: [],
	status: ''
  },
      methods: {
		  
        getPriceNamesList: function() {
            
                var dataURL = '/api/1.0/get_price_names';
				axios
                     .get(dataURL)
                     .then(response => (this.priceNamesList = response.data));
            
        },			  
        delPriceByName: function(name) {
			var arr = this.priceNamesList;
	
			for( var i = 0; i < arr.length; i++){ 
			   if ( arr[i] === name) {
				   
                var dataURL = '/api/1.0/del_price_by_name';
                dataURL = dataURL + '?comp_name=' + arr[i];
				axios.get(dataURL);						   
				   
				 arr.splice(i, 1); 
			   }
			}		
				
				
				
        },		  
		  
		  
        uploadFiles: function() {
          var s = this
          const data = new FormData(document.getElementById('uploadForm'))
          var imagefile = document.querySelector('#file')
//          console.log(imagefile.files[0])
          data.append('file', imagefile.files[0])
          data.append('name', s.name)
          data.append('email', s.email)
          axios.post('http://ztest.pp.ua/uploader', data, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
            .then(response => {
            //  console.log(response)
			  this.status = response.data;
            })
            .catch(error => {
              this.status = error.response.data;
            })
        }
      },
	  mounted () {
		this.getPriceNamesList()
 
	},
})
