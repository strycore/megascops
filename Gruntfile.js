module.exports = function(grunt) {
  grunt.initConfig({ 
    pkg: grunt.file.readJSON('package.json'),
    copy: {
      main: {
        files: [
          {flatten: true, expand: true, cwd: 'components/mediaelement/build/', src: '**', dest: 'public/mediaelement/'},
          {flatten: true, expand: true, cwd: 'components/jquery/dist/', src: '**', dest: 'public/js/'},
          {flatten: false, expand: true, cwd: 'components/bootstrap/dist/', src: '**', dest: 'public/'}
        ]
      }
    },
    coffee: {
      compile: {
        files: {
          'public/js/megascops.js': 'src/coffee/megascops.coffee'        
        }
      } 
    }
  });

  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-coffee');
  grunt.loadNpmTasks('grunt-contrib-copy'); 

  grunt.registerTask('default', ['coffee', 'copy']);
};
