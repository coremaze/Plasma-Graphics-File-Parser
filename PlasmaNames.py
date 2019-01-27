objectNames = (
        "Attribute",
        "Attribute.sequence",
        "Attribute.sequence.key",

        "Button",
        
        "Display",
        "Display.visibility",
        "Display.clipping",
        "Display.fillColor",
        "Display.strokeColor",
        "Display.blurRadius",

        "Edit",

        "SmoothMeshShape",

        "SmoothMeshShape.texture",
        "SmoothMeshShape.vertexPositions",
        "SmoothMeshShape.vertexColors",
        "SmoothMeshShape.vertexTexCoords",
        "SmoothMeshShape.extrusionMatrix",
        "SmoothMeshShape.extrusionBackColors",
        "SmoothMeshShape.extrusionFrontColors",
        "SmoothMeshShape.strokeColors",
        "SmoothMeshShape.strokeWidths",
        "SmoothMeshShape.strokeTexture",
        "SmoothMeshShape.textureTranslation",
        "SmoothMeshShape.textureRotation",
        "SmoothMeshShape.textureDeformation",
        "SmoothMeshShape.texturePivot",
        "SmoothMeshShape.textureOpacity",
        "SmoothMeshShape.textureBrightness",
        "SmoothMeshShape.textureContrast",
        "SmoothMeshShape.textureSaturation",
        "SmoothMeshShape.strokeTextureOpacity",
        "SmoothMeshShape.strokeTextureBrightness",
        "SmoothMeshShape.strokeTextureContrast",
        "SmoothMeshShape.strokeTextureSaturation",
        "SmoothMeshShape.strokeTextureStretch",
        
        "TextShape",
        "TextShape.color",
        "TextShape.strokeColor",
        "TextShape.extrusionColor",
        "TextShape.string",
        
        "Transformation",
        "Transformation.translation",
        "Transformation.rotation",
        "Transformation.pivot",
        "Transformation.deformation",
        
        "Node",
        "Widget",
        "ScrollButton",
        "ScrollSlider",
        "ArrayAttribute",
        "PopUpButton",
        "ListWidget",
        "Texture",
)

INT_TYPES = ('PlasmaGraphics',
             'ArrayAttribute.size',
             'SmoothMeshShape.subdivisions',
             'SmoothMeshShape.strokeJointType',
             'SmoothMeshShape.strokeCapType',
             'Node.widget',
             'Node.child',
             'Node.shape',
             'Node.transformation',
             'Node.display',
             'Texture.id',
             'Texture.format.pixelFormat',
             'Texture.width',
             'Texture.height',
             'SmoothMeshShape.strokeAlignment',
             'SmoothMeshShape.strokePattern',
             'Attribute.sequence.key.time')

UINT_TYPES = ('SmoothMeshShape.flags',
              'TextShape.flags',
              'Node.flags',
              'Widget.flags',
              'Button.type',
              'Display.flags',
              'Attribute.sequence.key.frame',
              'Texture.format.minFilter',
              'Texture.format.maxFilter',
              'Texture.format.horizontalWrap',
              'Texture.format.verticalWrap')

LENGTH_PREFIXED_WSTRING_TYPES = ('TextShape.wfontName',
                                 'Widget.caption',
                                 'SmoothMeshShape.wname',
                                 'TextShape.wname',
                                 'Transformation.wname',
                                 'Display.wname',
                                 'Node.wname',
                                 'Texture.wname',
                                 'Attribute.sequence.wname',
                                 'Widget.wname')

FLOAT_TYPES = ('SmoothMeshShape.smoothWeight',
               'SmoothMeshShape.strokeDash',
               'TextShape.pixelSize',
               'TextShape.strokeRadius',
               'dpi',
               'unit',
               'TextShape.wrapWidth',
               'pageWidth',
               'pageHeight',
               'SmoothMeshShape.strokeGap',
               'Widget.horizontalAlignment',
               'Widget.verticalAlignment',
               'TextShape.wrapWidth',
               'TextShape.spacing',
               'TextShape.lineSpacing',
               'Attribute.sequence.key.smoothness')

FLOAT_ARRAY_TYPES = ('pageColor',
                     'Widget.bindPos',
                     'Widget.innerBindPos',
                     'Widget.bindSize',
                     'Widget.framePos',
                     'Widget.frameSize',
                     'Widget.bindMatrix',
                     'Widget.innerBindSize')

UINT_ARRAY_TYPES = ('SmoothMeshShape.face',
                    'SmoothMeshShape.vertexFlags',
                    'SmoothMeshShape.vertexParameters')

#for Attribute.frame
FLOAT_ATTRIBUTE_CONTAINERS = ('SmoothMeshShape.textureDeformation',
                              'SmoothMeshShape.textureOpacity',
                              'SmoothMeshShape.textureBrightness',
                              'SmoothMeshShape.textureContrast',
                              'SmoothMeshShape.textureSaturation',
                              'SmoothMeshShape.strokeTextureOpacity',
                              'SmoothMeshShape.strokeTextureBrightness',
                              'SmoothMeshShape.strokeTextureContrast',
                              'SmoothMeshShape.strokeTextureSaturation',
                              'SmoothMeshShape.strokeTextureStretch',
                              'SmoothMeshShape.extrusionMatrix',
                              'TextShape.color',
                              'TextShape.strokeColor',
                              'TextShape.extrusionColor',
                              'Transformation.deformation',
                              'Transformation.translation',
                              'Transformation.pivot',
                              'Display.fillColor',
                              'Display.strokeColor',
                              'Display.blurRadius',
                              'SmoothMeshShape.textureTranslation',
                              'SmoothMeshShape.textureRotation',
                              'SmoothMeshShape.texturePivot',
                              'Transformation.rotation')
#for Attribute.frame
LENGTH_PREFIXED_WSTRING_ATTRIBUTE_CONTAINERS = ('TextShape.string')
#for Attribute.frame
INT_ATTRIBUTE_CONTAINERS = ('SmoothMeshShape.strokeTexture',
                            'SmoothMeshShape.texture',
                            'Display.visibility',
                            'Display.clipping')


FLOAT_ARRAYATTRIBUTE_CONTAINERS = ('SmoothMeshShape.strokeWidths',
                                   'SmoothMeshShape.extrusionBackColors',
                                   'SmoothMeshShape.extrusionFrontColors',
                                   'SmoothMeshShape.strokeColors',
                                   'SmoothMeshShape.vertexColors',
                                   'SmoothMeshShape.vertexTexCoords',
                                   'SmoothMeshShape.vertexPositions')
