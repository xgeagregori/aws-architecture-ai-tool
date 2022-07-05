import Head from "next/head";
import { useEffect, useState } from "react";
import axios from "axios";
import Image from "next/image";
import LoadingSpinner from "../components/LoadingSpinner";

interface HomeProps {
  apiUrl: string;
}

const CHARACTER_LIMIT = 345;
const TEXT_GRADIENT_STYLE =
  "text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-amber-400";

const Home: React.FC<HomeProps> = (props) => {
  const [prompt, setPrompt] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [diagram, setDiagram] = useState("");

  const onSubmit = async () => {
    setDiagram("");
    setIsLoading(true);

    const awsServicesTextData = (
      await axios.get(`${props.apiUrl}/aws-services?prompt=${prompt}`)
    ).data;

    console.log(awsServicesTextData.aws_services);

    const awsServicesDiagram = (
      await axios.get(`${props.apiUrl}/diagram?services=${awsServicesTextData.aws_services}`)
    ).data;

    setDiagram(awsServicesDiagram);
  };

  useEffect(() => {
    if (diagram) {
      setIsLoading(false);
    }
  }, [diagram]);

  return (
    <div className="flex justify-center items-center h-screen">
      <Head>
        <title>AWS Architecture AI Tool</title>
        <meta
          name="description"
          content="Generate AWS Services for your need."
        />
        <link rel="icon" href="/img/logo.svg" />
      </Head>

      <div className="mx-36 p-6 bg-slate-100 rounded-lg">
        <div className="flex items-center mb-6">
          <Image src="/img/logo.svg" width={64} height={64} alt="logo" />

          <div className="flex flex-col ml-4">
            <h1
              className={
                " text-center font-open font-semibold text-5xl " +
                TEXT_GRADIENT_STYLE
              }
            >
              AWS Architecture AI Tool
            </h1>

            <p className={TEXT_GRADIENT_STYLE + " text-lg font-semibold"}>
              Generate AWS Services for your need
            </p>
          </div>
        </div>
        <p className="text-gray-800 font-semibold text-lg">
          Tell me what your app is about and I will generate a list of the AWS
          Services you need to build it.
        </p>

        <div className="mt-4 mb-2">
          <textarea
            className="p-2 w-full rounded-md outline outline-2 outline-slate-300 focus:outline-amber-400 overflow-hidden resize-none text-gray-800 min-h-36 h-36 font-semibold"
            placeholder="I want to build an e-commerce app. It needs to be highly available. I need to store survey results. I need to use survey results to find the best fit from our database, I need to store purchase transactions. I need a chatbot to guide users."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            maxLength={CHARACTER_LIMIT}
          ></textarea>
          <div className="text-gray-800 font-semibold text-end">
            {prompt.length}/{CHARACTER_LIMIT}
          </div>
        </div>

        <button
          className="bg-gradient-to-r from-orange-400 to-amber-400 w-full py-2 rounded-md mt-4 text-white font-bold text-lg hover:opacity-80"
          onClick={onSubmit}
        >
          Submit
        </button>
        {isLoading && <LoadingSpinner />}
        {diagram && (
          <img src={`data:image/png;base64,${diagram}`} alt="diagram" />
        )}
      </div>
    </div>
  );
};

export function getStaticProps() {
  return {
    props: {
      apiUrl: process.env.REACT_APP_API_URL ?? "",
    },
  };
}

export default Home;
