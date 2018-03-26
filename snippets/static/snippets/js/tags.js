

function uuidv4() {
  return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
  )
}

function create_tag_label( tag, parent, onClose ) {

  var span = $(`<span class="tag label label-default">${tag.name} </span>`);
  span.css('background', tag.color);
  var cbtn = $('<button type="button" class="tag-close">&times;</button>');
  var onClose = onClose || function(){};
  cbtn.on('click', function(){ 
    span.remove();
    console.log(onClose); 
    onClose(); 
  });
  span.append(cbtn);
  if ( parent )
    $( parent ).append(span);
  return span;

}

function Tag(name='', id=null, color=null){
  var self = this;
  var color = color || '#cccccc';
  self.name = name;
  self.id = id;
  self.color = color;
}

function Tags(){
  
  var self = this;

  self.itemsById = {};
  self.itemsByName = {};

  self.pull = function() {
    $.ajax({
      method: 'GET',
      url : '/snippets/tags/all/',
      dataType: 'json',
      async: false,
      success: function( response ) {
        if ( response.status == 'ok' ) {
          self.itemsById = {};
          for ( var i = 0; i < response.msg.tags.length; i++ ) {
            var tag = response.msg.tags[ i ];
            tag = new Tag(tag.name, tag.id, tag.color);
            self.itemsById[ tag.id ] = tag;
            self.itemsByName[ tag.name ] = tag;
          }
        } else {
          console.log( response );
        }
      }
    });
  }

  self.add = function( names ) {

    var names = Array.isArray(names) ? names : [names];
    console.log('Adding tags to db:', names);
       
    return $.ajax({
      method: 'POST',
      url: '/snippets/tags/add/',
      data: {
        names : names,
      },
      async: false,
      dataType: 'json',
      success: function( response ) {
        console.log( response );
        if ( response.status == 'ok' ) {
          for ( var i = 0; i < response.msg.tags.length; i++ ) {
            var tag = response.msg.tags[ i ];
            self.itemsById[ tag.id ] = tag;
            self.itemsByName[ tag.name ] = tag;
          }
        }
      }
    });
  }

  self.exists = function( name ) {
    return name in self.itemsByName;
  }

}

function TagField( dom_element, opt ) {
  
  var self = this;
  var opt = opt || {};
  var tags = opt.tags || [];
  var datalist_id = opt.datalist;
  var datalist_attr = '';

  self.root = $( dom_element );

  // if datalist is not defined, try to get it from the dom
  if (! datalist_id)
    datalist_id = self.root.attr('datalist'); 

  if ( $( '#' + datalist_id ).length )
    datalist_attr = `list="${datalist_id}"`;
  
  // we have an array and a dictionary holding tag objects
  self.tags = [];
  self.byname = {};

  // create the dom elements for the field
  self.tagdiv = $('<div class="tag-div"></div>');
  self.edt = $(`<input type="text" class="tag-input" placeholder="Add tag.." ${datalist_attr}></input>`);
  self.root.append(self.tagdiv);
  self.root.append(self.edt);

  self.addElement = function( newTagName, id, color ) {

    var newTag = new Tag( newTagName, id, color );
    
    // create the label
    create_tag_label( newTag, self.tagdiv, function(){
    
      console.log( 'closing function called', self); 
      // this is called when the delete button of the label is clicked
      // remove from tags
      self.tags = self.tags.filter( function( el ) {
        return el.name !== newTagName;
      });
      // remove from byname
      delete self.byname[ newTagName ];
    
    });

    // add to internal structures
    self.tags.push( newTag );
    self.byname[ newTagName ] = newTag;    

  }

  // // add the starting tags, if present
  for (var i = 0; i < tags.length; i++) {
    self.addElement( tags[i].name, tags[i].id, tags[i].color );
  }

  // create a new tag label when unfocusing
  function unfocus(){

    var newTagName = self.edt.val();
    if ( newTagName.length && ! ( newTagName in self.byname ) )
      self.addElement( newTagName );
    self.edt.val( '' );

  }

  self.edt.on('blur', unfocus);

  // prevent unfocus on tab
  self.edt.on('keydown', function( e ) {
    if( e.which == 9 ) {
      if(e.preventDefault) {
        e.preventDefault();
      }
      return false;
    }
  });

  // add the tag when tab is released, while keeping focus on the edit field
  self.edt.on('keyup', function( e ) {
      e.preventDefault();
      if( e.which == 9 ) {
          unfocus();
          self.edt.focus();
      }
    } 
  );


}