import { useState } from "react";
import { login } from "@/stores/authStore";
import getFastApiErrorMessage from "@/utils/apiError";
import { AuthLayout } from "@/components/auth/AuthLayout";
import { AuthField } from "@/components/auth/AuthField";
import { AuthButton } from "@/components/auth/AuthButton";

export default function loginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async () => {
    setIsLoading(true);
    try {
      await login(email, password);
    } catch (err) {
      setError(getFastApiErrorMessage(err, "Could not sign in."));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthLayout
      subtitle="Sign In To Access Your Finances"
      footerHref="/register"
      footerLinkText="Sign Up"
      footerPrompt="Dont Have An Account?"
      error={error}
    >
      <AuthField
        label="Email"
        placeholder="Email Address"
        keyboardType="email-address"
        autoCapitalize="none"
        value={email}
        onChangeText={setEmail}
      ></AuthField>
      <AuthField
        label="Password"
        placeholder="Password"
        autoCapitalize="none"
        value={password}
        onChangeText={setPassword}
      ></AuthField>
      <AuthButton isLoading={isLoading} onPress={handleSubmit} title="Log In" />
    </AuthLayout>
  );
}
