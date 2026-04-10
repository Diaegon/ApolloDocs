import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi, describe, it, expect } from "vitest";
import { InversoresClient } from "../app/(dashboard)/dashboard/inversores/client";

// Mock Next.js router
vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: vi.fn(),
    back: vi.fn(),
    forward: vi.fn(),
  }),
}));

const mockData = [
  {
    brand: "CANADIAN",
    models: [
      {
        name: "CSI-5K-S22002-E",
        files: ["INMETRO - Canadian CSI-5K-S22002-E.pdf"],
      },
    ],
  },
  {
    brand: "GROWATT",
    models: [
      {
        name: "MIN 5000 TL-X",
        files: ["Growatt_MIN_5000.pdf"],
      },
    ],
  },
];

describe("InversoresClient", () => {
  it("renders the fetched data cleanly", async () => {
    render(<InversoresClient data={mockData} />);

    // Wait for the data to be loaded and rendered
    await waitFor(() => {
      expect(screen.getByText(/CANADIAN/i)).toBeInTheDocument();
      expect(screen.getByText(/GROWATT/i)).toBeInTheDocument();
    });

    // Click to expand the CANADIAN brand accordion
    await userEvent.click(screen.getByText(/CANADIAN/i));

    // Check if the CANADIAN models and files are rendered
    expect(screen.getByText("CSI-5K-S22002-E")).toBeInTheDocument();
    expect(
      screen.getByText("INMETRO - Canadian CSI-5K-S22002-E.pdf")
    ).toBeInTheDocument();

    // Click to expand the GROWATT brand accordion
    await userEvent.click(screen.getByText(/GROWATT/i));
    expect(screen.getByText("MIN 5000 TL-X")).toBeInTheDocument();
  });
});
