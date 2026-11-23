import { useState } from "react";
import { register } from "@/stores/authStore";
import getFastApiErrorMessage from "@/utils/apiError";
import { AuthLayout } from "@/components/auth/AuthLayout";
import { AuthField } from "@/components/auth/AuthField";
import { AuthButton } from "@/components/auth/AuthButton";

export default function registerPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async () => {
    setIsLoading(true);
    try {
      await register(email, password, first_name, last_name);
    } catch (err) {
      setError(getFastApiErrorMessage(err, "Could not sign up."));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthLayout
      subtitle="Sign In To Access Your Finances"
      footerHref="/login"
      footerLinkText="Sign In"
      footerPrompt="Already Have An Account?"
    >
      <AuthField
        label="Email"
        placeholder="Email Address"
        keyboardType="email-address"
        autoCapitalize="none"
        value={email}
        onChangeText={setEmail}
      />
      <AuthField
        label="First Name"
        placeholder="First Name"
        autoCapitalize="none"
        value={first_name}
        onChangeText={setFirstName}
      />
      <AuthField
        label="Last Name"
        placeholder="Last Name"
        autoCapitalize="none"
        value={last_name}
        onChangeText={setLastName}
      />
      <AuthField
        label="Password"
        placeholder="Password"
        autoCapitalize="none"
        value={password}
        onChangeText={setPassword}
      />
      <AuthButton isLoading={isLoading} onPress={handleSubmit} title="Log In" />
    </AuthLayout>
  );
}
