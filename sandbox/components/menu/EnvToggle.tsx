import { useContext, useState } from "react";

import { AuthContext } from "./Auth";
import { Button } from "../inputs/Button";
import { Environment } from "../../lib/utilities/environmentUtilities";
import { useRouter } from "next/router";

type EnvToggleProps = {
  className?: string;
};

export function EnvToggle({ className }: EnvToggleProps) {
  const authContext = useContext(AuthContext);
  const [open, setOpen] = useState(false);

  return (
    <div className={`${className}`}>
      {open && (
        <div className="flex">
          <EnvButton name="Dev" environment={Environment.Dev} onSelect={() => setOpen(false)} />
          <EnvButton name="Test" environment={Environment.Test} onSelect={() => setOpen(false)} />
          <EnvButton name="Prod" environment={Environment.Prod} onSelect={() => setOpen(false)} />
        </div>
      )}
      {!open && (
        <div>
          <Button
            className={`mr-2 text-center text-sm capitalize`}
            text={authContext.environment}
            onClick={() => setOpen(true)}
            tooltip="Switch environment"
          />
        </div>
      )}
    </div>
  );
}

type EnvButtonProps = {
  name: string;
  environment: Environment;
  onSelect: () => void;
};

export function EnvButton({ name, environment, onSelect }: EnvButtonProps) {
  const authContext = useContext(AuthContext);
  const router = useRouter();

  function onClick() {
    authContext.setEnvironment(environment);
    onSelect();

    if (environment != authContext.environment) {
      router.reload();
    }
  }

  const variant = authContext.environment === environment ? "primary" : "secondary";

  return <Button variant={variant} className="mr-2 text-center text-sm" text={name} onClick={onClick} />;
}
