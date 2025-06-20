import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Box, Text, Image, VStack, Icon } from '@chakra-ui/react';
import { FiUpload } from 'react-icons/fi';

interface ImageUploadProps {
  onImageSelect: (file: File) => void;
  previewUrl?: string;
}

const ImageUpload: React.FC<ImageUploadProps> = ({ onImageSelect, previewUrl }) => {
  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      if (acceptedFiles.length > 0) {
        onImageSelect(acceptedFiles[0]);
      }
    },
    [onImageSelect]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png']
    },
    maxFiles: 1,
  });

  return (
    <Box
      {...getRootProps()}
      w="full"
      h="300px"
      border="2px dashed"
      borderColor={isDragActive ? 'brand.500' : 'gray.200'}
      borderRadius="lg"
      bg={isDragActive ? 'brand.50' : 'white'}
      transition="all 0.2s"
      cursor="pointer"
      _hover={{
        borderColor: 'brand.500',
        bg: 'brand.50',
      }}
    >
      <input {...getInputProps()} />
      <VStack h="full" justify="center" spacing={4}>
        {previewUrl ? (
          <Image
            src={previewUrl}
            alt="Preview"
            maxH="250px"
            objectFit="contain"
            borderRadius="md"
          />
        ) : (
          <>
            <Icon as={FiUpload} w={10} h={10} color="gray.400" />
            <Text color="gray.500" fontSize="lg" textAlign="center">
              {isDragActive
                ? 'Drop the image here'
                : 'Drag and drop an image here, or click to select'}
            </Text>
          </>
        )}
      </VStack>
    </Box>
  );
};

export default ImageUpload; 