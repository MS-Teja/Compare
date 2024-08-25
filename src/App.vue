<template>
  <div id="app">
    <h1>Price Comparison</h1>
    <ProductSearch />
  </div>
</template>

<script>
import ProductSearch from './components/ProductSearch.vue';

export default {
  name: 'App',
  components: {
    ProductSearch
  }
};
</script>

<style>
h1 {
    text-align: center;
    color: #808080;
}
</style>