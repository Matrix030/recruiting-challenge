import React, { useState } from 'react';
import {
  Box,
  Button,
  Heading,
  Text,
  VStack,
  useToast,
  Card,
  CardBody,
} from '@chakra-ui/react';
import ImageUpload from '../components/ImageUpload';
import { createProfile } from '../services/api';

const CreateProfile = () => {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [profile, setProfile] = useState<any>(null);
  const toast = useToast();

  const handleImageSelect = (file: File) => {
    setSelectedImage(file);
    setPreviewUrl(URL.createObjectURL(file));
    setProfile(null);
  };

  const handleSubmit = async () => {
    if (!selectedImage) return;

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', selectedImage);

      const response = await createProfile(formData);
      setProfile(response);
      toast({
        title: 'Profile Created',
        description: 'Face profile has been successfully created.',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to create face profile. Please try again.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <VStack spacing={8} align="stretch">
        <Box textAlign="center">
          <Heading size="xl" color="brand.700" mb={4}>
            Create Face Profile
          </Heading>
          <Text fontSize="lg" color="gray.600">
            Upload a photo to generate a detailed face profile with measurements and features.
          </Text>
        </Box>

        <ImageUpload onImageSelect={handleImageSelect} previewUrl={previewUrl || undefined} />

        <Button
          size="lg"
          isLoading={loading}
          onClick={handleSubmit}
          isDisabled={!selectedImage}
        >
          Create Profile
        </Button>

        {profile && (
          <Card>
            <CardBody>
              <VStack align="stretch" spacing={4}>
                <Heading size="md" color="brand.700">
                  Profile Details
                </Heading>
                <Text>
                  <strong>Profile ID:</strong> {profile.id}
                </Text>
                <Text>
                  <strong>Description:</strong> {profile.description}
                </Text>
                <Text>
                  <strong>Created:</strong>{' '}
                  {new Date(profile.created_at).toLocaleString()}
                </Text>
              </VStack>
            </CardBody>
          </Card>
        )}
      </VStack>
    </Box>
  );
};

export default CreateProfile; 