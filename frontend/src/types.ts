export const STATUSES = ['APPROVED', 'EXPIRED', 'SUSPENDED', 'ALL'] as const;
export type QueryStatus = typeof STATUSES[number];

export interface Facility {
  locationid: number;
  Applicant: string;
  Status: string;      // or QueryStatus if your backend only returns these
  Address: string;
  Latitude: number;
  Longitude: number;
  DistanceKm?: number; // present on "nearest" endpoint
}

export interface SearchApplicantParams {
  applicant: string;
  status?: QueryStatus;
}

export interface SearchApplicantFormProps {
  onSearch: (params: SearchApplicantParams) => void;
}