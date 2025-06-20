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
  Progress,
  HStack,
  NumberInput,
  NumberInputField,
  FormControl,
  FormLabel,
} from '@chakra-ui/react';
import ImageUpload from '../components/ImageUpload';
import { verifyFace } from '../services/api';

const VerifyFace = () => {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [profileId, setProfileId] = useState<number>(1);
  const toast = useToast();

  const handleImageSelect = (file: File) => {
    setSelectedImage(file);
    setPreviewUrl(URL.createObjectURL(file));
    setResult(null);
  };

  const handleSubmit = async () => {
    if (!selectedImage) return;

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', selectedImage);

      const response = await verifyFace(profileId, formData);
      setResult(response);
      toast({
        title: response.is_match ? 'Match Found' : 'No Match',
        description: `Similarity score: ${(response.score * 100).toFixed(2)}%`,
        status: response.is_match ? 'success' : 'warning',
        duration: 5000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to verify face. Please try again.',
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
            Verify Face
          </Heading>
          <Text fontSize="lg" color="gray.600">
            Compare a photo against an existing face profile to verify identity.
          </Text>
        </Box>

        <FormControl>
          <FormLabel>Profile ID to verify against</FormLabel>
          <NumberInput
            min={1}
            value={profileId}
            onChange={(_, value) => setProfileId(value)}
          >
            <NumberInputField />
          </NumberInput>
        </FormControl>

        <ImageUpload onImageSelect={handleImageSelect} previewUrl={previewUrl || undefined} />

        <Button
          size="lg"
          isLoading={loading}
          onClick={handleSubmit}
          isDisabled={!selectedImage}
        >
          Verify Face
        </Button>

        {result && (
          <Card>
            <CardBody>
              <VStack align="stretch" spacing={6}>
                <Heading size="md" color="brand.700">
                  Verification Result
                </Heading>
                
                <Box>
                  <HStack justify="space-between" mb={2}>
                    <Text fontWeight="bold">Similarity Score</Text>
                    <Text>{(result.score * 100).toFixed(2)}%</Text>
                  </HStack>
                  <Progress
                    value={result.score * 100}
                    colorScheme={result.is_match ? 'green' : 'orange'}
                    borderRadius="full"
                    size="lg"
                  />
                </Box>

                <Text
                  fontSize="xl"
                  fontWeight="bold"
                  color={result.is_match ? 'green.500' : 'orange.500'}
                >
                  {result.is_match ? 'Match Found ✓' : 'No Match ✗'}
                </Text>
              </VStack>
            </CardBody>
          </Card>
        )}
      </VStack>
    </Box>
  );
};

export default VerifyFace; 