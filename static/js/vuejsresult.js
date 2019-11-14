
Vue.component('result-grid', {
    template: '#resultGridTemplate',
    props: {
        dataresult: Array,
        columns: Array,
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
            var dataresult = this.dataresult

            if (sortKey) {
                dataresult = dataresult.slice().sort(function(a, b) {
                    a = a[sortKey]
                    b = b[sortKey]
                    return (a === b ? 0 : a > b ? 1 : -1) * order
                })
            }
            return dataresult
        }
    },
    filters: {
		capitalize: function (value) {
		if (value === '1main_price') return 'Основной прайс лист';
		else {return value}
	}
    },
    methods: {
        sortBy: function(key) {
            this.sortKey = key
            this.sortOrders[key] = this.sortOrders[key] * -1
        },		
		delRow: function(element) {
			var arr = this.dataresult;
	
			for( var i = 0; i < arr.length; i++){ 
			   if ( arr[i] === element) {
				   
                var dataURL = '/api/1.0/delete_result';
                dataURL = dataURL + '?id=' + arr[i].res_id[0];
				axios.get(dataURL);						   
				   
				   
				 arr.splice(i, 1); 
			   }
			}
			
		}

    }
})




var ResultTable = new Vue({
    el: '#ResultTable',
    data: {
        gridRColumns: ['id', 'name', 'price','diff'],
        gridRData: [] 
    },
    methods: {
		readResult: function() {
			    var dataURL = '/api/1.0/read_result';
				axios
                    .get(dataURL)
                    .then(response => (this.gridRData = response.data));
					
		},		

	
	},
	filters: {

},
	mounted() {
		this.readResult();
	}
	
	
})