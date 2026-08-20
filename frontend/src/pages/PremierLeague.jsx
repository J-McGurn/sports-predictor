import { useEffect, useState } from "react";
import {
  DndContext,
  closestCenter,
  PointerSensor,
  useSensor,
  useSensors,
} from "@dnd-kit/core";
import {
  arrayMove,
  SortableContext,
  verticalListSortingStrategy,
  useSortable,
} from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import "./Sport.css";

import {
  getActiveSeasons,
  getPLTeams,
  getPLPrediction,
  savePLPrediction,
} from "../services/api";


function SortableTeam({ team, position }) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
  } = useSortable({
    id: team.id,
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      className="prediction-row"
    >
      <div className="prediction-position">
        {position}
      </div>

      <div className="prediction-team">
        {team.name}
      </div>

      <button
        type="button"
        className="drag-handle"
        {...attributes}
        {...listeners}
        aria-label={`Move ${team.name}`}
      >
        ☰
      </button>
    </div>
  );
}


function PremierLeague() {
  const [season, setSeason] = useState(null);
  const [teams, setTeams] = useState([]);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 5,
      },
    })
  );


  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        setError("");

        const seasonData = await getActiveSeasons();

        const premierLeagueSeason =
          seasonData.seasons.find(
            (season) => season.sport === "PL"
          );

        if (!premierLeagueSeason) {
          throw new Error(
            "No active Premier League season found."
          );
        }

        setSeason(premierLeagueSeason);

        const teamData = await getPLTeams(
          premierLeagueSeason.id
        );

        let loadedTeams = teamData.teams;

        /*
         * Try to load an existing prediction.
         *
         * If the user has already submitted one,
         * display it in their saved order.
         */
        try {
          const predictionData =
            await getPLPrediction(
              premierLeagueSeason.id
            );

          if (
            predictionData.predictions &&
            predictionData.predictions.length === 20
          ) {
            loadedTeams =
              predictionData.predictions.map(
                (prediction) => prediction.team
              );
          }
        } catch {
          /*
           * No existing prediction is fine.
           * We'll simply use the default team order.
           */
        }

        setTeams(loadedTeams);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);


  function handleDragEnd(event) {
    const { active, over } = event;

    if (!over || active.id === over.id) {
      return;
    }

    setTeams((currentTeams) => {
      const oldIndex = currentTeams.findIndex(
        (team) => team.id === active.id
      );

      const newIndex = currentTeams.findIndex(
        (team) => team.id === over.id
      );

      return arrayMove(
        currentTeams,
        oldIndex,
        newIndex
      );
    });

    setSuccess("");
  }


  async function handleSave() {
    if (!season || teams.length !== 20) {
      return;
    }

    try {
      setSaving(true);
      setError("");
      setSuccess("");

      const predictions = teams.map(
        (team, index) => ({
          team_id: team.id,
          position: index + 1,
        })
      );

      await savePLPrediction(
        season.id,
        predictions
      );

      setSuccess(
        "Your Premier League prediction has been saved."
      );
    } catch (error) {
      setError(error.message);
    } finally {
      setSaving(false);
    }
  }


  if (loading) {
    return (
      <main className="sport-page">
        <div className="sport-page-container">
          <p>Loading Premier League...</p>
        </div>
      </main>
    );
  }


  if (error && !season) {
    return (
      <main className="sport-page">
        <div className="sport-page-container">
          <div className="auth-error">
            {error}
          </div>
        </div>
      </main>
    );
  }


  return (
    <main className="sport-page">
      <div className="sport-page-container">

        <header className="sport-page-header">
          <h1>Premier League</h1>

          <p>
            Predict the final table for{" "}
            <strong>{season.name}</strong>.
          </p>
        </header>


        {error && (
          <div className="auth-error">
            {error}
          </div>
        )}


        {success && (
          <div className="prediction-success">
            {success}
          </div>
        )}


        <section className="prediction-section">

          <div className="prediction-instructions">
            <h2>Your prediction</h2>

            <p>
              Drag the teams into the position you
              think they will finish.
            </p>
          </div>


          <DndContext
            sensors={sensors}
            collisionDetection={closestCenter}
            onDragEnd={handleDragEnd}
          >
            <SortableContext
              items={teams.map(
                (team) => team.id
              )}
              strategy={
                verticalListSortingStrategy
              }
            >

              <div className="prediction-table">

                <div className="prediction-table-header">
                  <span>Position</span>
                  <span>Team</span>
                  <span></span>
                </div>

                {teams.map(
                  (team, index) => (
                    <SortableTeam
                      key={team.id}
                      team={team}
                      position={index + 1}
                    />
                  )
                )}

              </div>

            </SortableContext>
          </DndContext>


          <div className="prediction-actions">
            <button
              type="button"
              onClick={handleSave}
              disabled={
                saving ||
                teams.length !== 20
              }
            >
              {saving
                ? "Saving..."
                : "Save Prediction"}
            </button>
          </div>

        </section>

      </div>
    </main>
  );
}

export default PremierLeague;