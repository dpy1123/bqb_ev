<template>
  <div id="app"> 
    <div class="window">
      <div class="window-content">
          <div class="pane-group">
            <div class="pane-mini sidebar">
                <div class="list-group">
                    <router-link class="nav-group-item" to="/list">
                      <span class="icon icon-folder icon-bg"></span>
                    </router-link>
                    <router-link class="nav-group-item" to="upload">
                      <span class="icon icon-upload icon-bg"></span>
                    </router-link>
                </div>
            </div>
                    
            <!-- content -->
            <router-view></router-view>  

          </div>
      </div>
    </div>
  </div>
</template>

<script>
  require('./libs/photon/css/photon.min.css')
  export default {
    name: 'bqb_ev'
  }
</script>

<style>
 .nav-group-item  .icon.icon-bg {
    font-size: 32px;
    width: inherit;
    height: inherit;
}
.input-text {
    display: inline-block;
    /* width: 100%; */
    min-height: 25px;
    padding: 4px 10px;
    font-size: 13px;
    /* line-height: 1.6; */
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 4px;
    outline: none;
    vertical-align: middle;
}
</style>
